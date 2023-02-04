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

product = get_product('8002270506833')
print (product)

def index(request):
    context = {}

    result = 1+1
    context["result"] = result
    return render(request, 'main.html', context)