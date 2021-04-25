from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Order, Product


class CreateUserForm(UserCreationForm):
  username = forms.CharField(max_length=30)
  first_name = forms.CharField(max_length=30)
  last_name = forms.CharField(max_length=30)
  email = forms.EmailField(max_length=50)
  address = forms.CharField()
  class Meta:
    model = User
    fields = [ 'first_name', 'last_name', 'username', 'email', 'password1', 'password2', 
        'address',]


class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','image_url', 'brand']