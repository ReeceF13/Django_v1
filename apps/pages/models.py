from django.db import models
from apps.models.base import BaseModel
from apps.models.core import Store, RegionalCoach, AreaCoach, BusinessPartner
# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=100, default="")
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
class Region_r(models.Model):
    region_name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.region_name
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
