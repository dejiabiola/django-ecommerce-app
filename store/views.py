from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
# Create your views here.


def user_login(request):
  return render(request, 'store/login.html')

def register(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      user.customer.first_name = form.cleaned_data.get('first_name')
      user.customer.last_name = form.cleaned_data.get('last_name')
      user.save()
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, 'account was created for ' + username )
      return redirect('/')
    else:
      print("Form is not valid")

  context = {'form': form}
  return render(request, 'store/register.html', context)

def index(request):
  products = Product.objects.all()
  context = {'products': products}
  return render(request, 'store/index.html', context)


def cart(request):
  user = request.user
  if user.is_authenticated:
    customer = user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 
    items = order.lineitem_set.all()
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  context = {'items': items, 'order': order}
  return render(request, 'store/cart.html', context)


def checkout(request):
  user = request.user
  if user.is_authenticated:
    customer = user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 
    items = order.lineitem_set.all()
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  context = {'items': items, 'order': order}
  return render(request, 'store/checkout.html', context)
