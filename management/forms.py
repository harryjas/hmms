from django import forms
from django.contrib.auth.models import User

from .models import Meal, Item


class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ['meal']


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['item_name', 'item_price']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
