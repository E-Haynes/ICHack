"""fridgehack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from core import views

urlpatterns = [
    path('', views.index, name="index"),
    path('register', views.start_flow, name="start_flow"),
    path('scan_a_product', views.scan_a_product, name="scan_a_product"),
    path('select_a_shelf/<str:upc>', views.select_a_shelf, name="select_a_shelf"),
    path('finish_addition/<str:upc>/<str:shelf_id>', views.finish_addition, name="finish_addition"),
    path('remove-item/<str:item_id>/', views.remove_item, name="remove_item"),
    path('list_view/', views.list_view, name="list_view"),
    path('yannis_test_view/', views.yannis_test_view, name='yannis_test_view'),
    path('generate_a_recipe', views.generate_a_recipe, name="generate_a_recipe"),
    path('view_recipe/<str:recipe_id>', views.view_recipe, name="view_a_recipe"),
    path('favourite_recipe/<str:recipe_id>', views.favourite_recipe, name="view_a_recipe"),
    path('recipes_listing/', views.recipes_listing, name="recipes_listing")


]
