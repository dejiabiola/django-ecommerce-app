from django.shortcuts import render
from .models import *
# Create your views here.


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
