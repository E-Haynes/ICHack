from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.core.paginator import Paginator
import datetime
from django.core.files.storage import FileSystemStorage
import uuid
from django.http.multipartparser import MultiPartParser
import json
from django.contrib.auth.models import User
from core.models import Fridge, Shelf, Recipe, UserProfile, UserAddedFoodItems
import django.contrib.auth as auth
import openfoodfacts
from django.contrib import messages
import openai

def index(request):
    context = {}
    context['shelves_fridge'] = Shelf.objects.filter(fridge__owner=request.user, freezer=False).order_by('number')
    context['shelves_freezer'] = Shelf.objects.filter(fridge__owner=request.user, freezer=True).order_by('number')
    context['shelf_items'] = {}
    for shelf in context['shelves_fridge']:
        context['shelf_items'][shelf.pk] = UserAddedFoodItems.objects.filter(on_shelf=shelf.pk)
    for shelf in context['shelves_freezer']:
        context['shelf_items'][shelf.pk] = UserAddedFoodItems.objects.filter(on_shelf=shelf.pk)
    return render(request, 'main.html', context)

def start_flow(request):
    context = {}
    if(request.method == 'GET'):
        return render(request, 'new_user.html', context)
    elif(request.method == 'POST'):
        print(request.POST)
        new_user = User.objects.create(first_name=request.POST['firstname'],last_name=request.POST['lastname'], email=request.POST['email'], username=request.POST['email'])
        user_fridge = Fridge.objects.create(owner = new_user)
        for shelf in range(int(request.POST['numberofshelvesfridge'])):
            Shelf.objects.create(fridge=user_fridge, number=shelf)
        for shelf in range(int(request.POST['numberofshelvesfreezer'])):
            Shelf.objects.create(fridge=user_fridge, freezer=True, number=shelf)
        auth.login(request, new_user)
        return redirect('/')

def scan_a_product(request):
    context = {}
    if(request.method == 'GET'):
        return render(request, 'scan_a_product.html', context)
    if(request.method == 'POST'):
        product = get_product(request.POST['upc'])
        return redirect('select_a_shelf/'+request.POST['upc'])

def select_a_shelf(request,upc):
    context = {}
    context['upc'] = upc
    context['product'] = get_product(upc)
    context['shelves_fridge'] = Shelf.objects.filter(fridge__owner=request.user, freezer=False).order_by('number')
    context['shelves_freezer'] = Shelf.objects.filter(fridge__owner=request.user, freezer=True).order_by('number')
    if(request.method == 'GET'):
        return render(request, 'select_a_shelf.html', context)
    # if(request.method == 'POST'):
    #     product = get_product(request.POST['upc'])
    #     return JsonResponse(product)

def remove_item(request, item_id):
    item_to_remove = UserAddedFoodItems.objects.get(pk=item_id)
    messages.error(request, f'{item_to_remove.productName} - {item_to_remove.brand} deleted.')
    item_to_remove.delete()

    return redirect('/')

def finish_addition(request,upc,shelf_id):
    context = {}
    context['upc'] = upc
    context['product'] = get_product(upc)
    product = context['product']
    context['shelf_id'] = shelf_id
    if(request.method == 'GET'):
        return render(request, 'finish_addition.html', context)
    if(request.method == 'POST'):
        UserAddedFoodItems.objects.create(owner = request.user,on_shelf = Shelf.objects.get(pk=shelf_id),brand = product['brand'], productName = product['productName'], weight = product['weight'], servingWeight = product['servingWeight'], labels = product['labels'], imageURL = product['imageURL'], expiry_date=request.POST['expiryDate'])
        return redirect('/')

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

def list_view(request):
    context = {}
    user_fridge = Fridge.objects.get(owner=request.user)
    print(user_fridge)
    context['list_of_items'] = UserAddedFoodItems.objects.filter(on_shelf__fridge=user_fridge).order_by('expiry_date')
    print(context['list_of_items'])
    return render(request, 'list_view.html', context)

openai.api_key = "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"

recipeCommand = ""

products1 = {
    "name":("apples", "lucozade", "coconuts"),
    "size":("200", None, "350")
}

def createPrompt(products):
    start = "Come up with a recipe with only a few ingredients from: "
    weight_name_connection = ' g of '
    mid = ""
    connector = " and "
    ending = " and nothing else.\n"
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



def yannis_test_view(request):
    user_fridge = Fridge.objects.get(owner=request.user)
    list_of_products= UserAddedFoodItems.objects.filter(on_shelf__fridge=user_fridge).order_by('expiry_date')

    products2 = {
    "name":[],
    "size":[]
    }
    for item in list_of_products:
        if(item.productName):
            products2['name'].append(item.productName)
        else:
            products2['name'].append(item.brand)

        products2['size'].append(item.weight)

    message = createPrompt(products2)
    recipes = createRecipes(f'{message} \n')

    return JsonResponse(recipes, safe=False)
