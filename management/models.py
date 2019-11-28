from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Meal(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    meal = models.CharField(max_length=250)

    def __str__(self):
        return self.meal


class Item(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=250)
    item_price = models.IntegerField()

    def __str__(self):
        return self.item_name
