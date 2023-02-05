from django.contrib import admin

# Register your models here.
from core.models import Fridge, Shelf, Recipe, UserProfile, UserAddedFoodItems, FavouriteRecipes

admin.site.register(Fridge)
admin.site.register(Shelf)
admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(UserAddedFoodItems)
admin.site.register(FavouriteRecipes)

