from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Order, Product


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']


class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','image_url', 'brand']