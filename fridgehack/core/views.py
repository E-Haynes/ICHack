from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator
import datetime
from django.core.files.storage import FileSystemStorage
import uuid
from django.http.multipartparser import MultiPartParser
import json

import requests
import openfoodfacts
import os
import openai

url = "https://api.edamam.com/api/food-database/v2/parser"
querystring = {"ingr":"apple", "nutrition-type":"cooking"#}
#headers = {
    ,"app_id": "93b12053",
    "app_key": "fd7991107f1cb3a1207293f622e6774b"
    }
#response = requests.get(url, params=querystring)
#print(response.text)

def get_product(code):
    d = dict()
    product = openfoodfacts.products.get_product(code)
    try:
        d['brand'] = product['product']['brands']
    except:
        d['brand'] = None
    try:
        d['productName'] = product['product']['product_name']
    except:
        d['productName'] = None
    try:
        d['weight'] = product['product']['product_quantity']
    except:
        d['weight'] = None
    try:
        d['servingWeight'] = product['product']['serving_quantity']
    except:
        d['servingWeight'] = None
    try:
        d['labels'] = product['product']['labels']
    except:
        d['labels'] = None
    try:
        d['imageURL'] = product['product']['image_url']
    except:
        d['imageURL'] = None
    return d

product = get_product('')
print (product)

openai.api_key = "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"

recipeCommand = ""

products1 = {
    "name":("strawberry", "chocolate", "marshmellows"),
    "size":("200", None, "350")
}

def createPrompt(products):
    start = "Come up with a recipe including "
    weight_name_connection = ' g of '
    mid = ""
    connector = " and "
    ending = " and nothing else."
    msg = ""

    for index, item in enumerate(products["name"]):
        if(index == 0):
            if(products["size"][index] is not None):
                mid = f'{products["size"][index]} g of {item}'
            else:
                mid = f'{item}'
        else:
            if(products["size"][index] is not None):
                mid = mid + connector + f'{products["size"][index]} g of {item}'
            else:
                mid = mid + connector + f'{item}'
            



    msg = start + mid + ending
    return msg


message = createPrompt(products1)
print(message)


def createRecipes(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0]['text']

recipes = createRecipes(f'{message} \n')
print(recipes)

recipeTitle = recipes.partition('\n')[2]
print(recipeTitle)

def recipeImage(prompt):
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


recipeImageURL = recipeImage(recipeTitle)
print(recipeImageURL)


def index(request):
    context = {}

    result = 1+1
    context["result"] = result
    return render(request, 'main.html', context)