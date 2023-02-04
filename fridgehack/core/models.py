from django.db import models
from django.contrib.auth.models import User


class Fridge(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return f'Fridge ({self.pk}) belonging to {self.owner}'



class Shelf(models.Model):
    fridge = models.ForeignKey(to=Fridge,on_delete=models.SET_NULL,blank=True,null=True)
    freezer = models.BooleanField(default=False)
    number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        frozen = "Fridge"
        if(self.freezer):
            frozen = "Freezer"
        return f'{frozen} Shelf ({self.pk}) number {self.number}  belonging to fridge {frozen} {self.fridge.pk}'

class UserAddedFoodItems(models.Model):
    owner = models.ForeignKey(to=User,on_delete=models.SET_NULL,blank=True,null=True)
    on_shelf = models.ForeignKey(to=Shelf,on_delete=models.SET_NULL,blank=True,null=True)
    brand = models.TextField(default="", null=True, blank=True)
    productName = models.TextField(default="", null=True, blank=True)
    weight = models.TextField(default="", null=True, blank=True)
    servingWeight = models.TextField(default="", null=True, blank=True)
    labels = models.TextField(default="", null=True, blank=True)
    imageURL = models.TextField(default="", null=True, blank=True)
    expiry_date= models.DateField(null=True,blank=True)

class Recipe(models.Model):
    title = models.CharField(max_length=200)

class UserProfile(models.Model):
    author = models.ForeignKey(to=User,on_delete=models.SET_NULL,blank=True,null=True)

# Create your models here.
