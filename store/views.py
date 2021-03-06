from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseServerError, Http404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm, ProductForm
from django.db.models import Q

class Basket:
  # a data transfer object to shift items from cart to page. Used for guest login only
  
  def __init__(self, id, name, price, image_url, quantity):
    self.id = id
    self.name = name
    self.price = price
    self.quantity = quantity
    self.image_url = image_url

  def get_total(self):
    return self.quantity * self.price


# Create your views here.

def error_400_view(request, exception):
    return HttpResponse("Bad request, probably not the right command?")

def error_404_view(request, exception):
    return HttpResponseNotFound("So sorry we could not find the page you were looking for")

def error_500_view(request):
    return HttpResponseServerError("Oops something went wront on our side. Sorry!")


# convenience method as used in several methods
def get_basket(request):
  basket = request.session.get('basket', [])
  products = []
  for item in basket:
    product = Product.objects.get(id=item[0])
    basket = Basket(item[0], product.name, product.price, product.image_url, item[1])
    products.append(basket)
  return products

def user_login(request):
  # if user is already logged in, don't show him the login page
  if request.user.is_authenticated:
    return redirect('index')
  else:
    try:
      del request.session['user']
    except KeyError:
      pass
    if request.method == 'POST':
      # user wants to login as guest, store that is sessions
      if request.POST['guest'] == 'guest':
        request.session['user'] = 'guest'
        guest_login = request.session['user']
        return redirect('/')

      else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user)
          # Redirect to a success page.
          if user.is_authenticated & user.is_staff:
            messages.success(request, 'You were logged in successfully as admin')
          else:
            messages.success(request, 'You were logged in successfully')
          return redirect('/')
        else:
          messages.error(request, 'Invalid username or password')

    return render(request, 'store/login.html')

def register(request):
  if request.user.is_authenticated:
    return redirect('index')
  else:
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
    return render(request, 'registration/register.html', context)

def logoutUser(request):
  logout(request)
  return redirect('login')

def index(request):
  try:
    guest_login = request.session['user']
  except KeyError:
    guest_login = None
  products = Product.objects.all()
  context = {'products': products, 'guest_login': guest_login}
  return render(request, 'store/index.html', context)

def product_detail(request, id):
  try:
    guest_login = request.session['user']
  except KeyError:
    guest_login = None
  product = get_object_or_404(Product, id=id)
  related_products = Product.objects.filter(brand=product.brand)
  context = {'product': product, 'guest_login': guest_login, "related_products": related_products}
  return render(request, 'store/product_detail.html', context)

def product_buy(request):
  try:
    guest_login = request.session['user']
  except KeyError:
    guest_login = None
  if guest_login == 'guest' or request.user.is_authenticated: 
    if request.method== "POST":
        product_id = int(request.POST.get('id',''))
        quantity = int(request.POST.get('quantity', ''))
        if request.user.is_authenticated:
          customer = request.user.customer
          product = Product.objects.get(id=product_id)
          order, created = Order.objects.get_or_create(customer=customer, complete=False) 
          line_item, created = LineItem.objects.get_or_create(order=order, product=product)
          line_item.quantity = quantity
          line_item.save()
        else:
          basket = request.session.get('basket', [])
          basket.append([product_id,quantity])
          request.session['basket'] = basket

    return redirect('index')
  else:
    messages.info(request, "Please login or continue as guest to purchase a product")
    return redirect('login')

def product_new(request):
    if request.method=="POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_date = timezone.now()
            product.save()
            messages.success(request, product.name + ' has been added successfully')
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm()
    return render(request, 'store/product_edit.html', {'form': form, 'new': 'new'})

def product_edit(request, id):
    user = request.user
    if user.is_superuser or user.is_staff:
      product = get_object_or_404(Product, id=id)
      if request.method=="POST":
          form = ProductForm(request.POST, instance=product)
          if form.is_valid():
              product = form.save(commit=False)
              product.created_date = timezone.now()
              product.save()
              messages.success(request, product.name + ' has been updated successfully')
              return redirect('product_detail', id=product.id)
      else:
          form = ProductForm(instance=product)
      return render(request, 'store/product_edit.html', {'form': form})
    else:
      return redirect('login')

#search from product
def product_search(request):
  try:
    guest_login = request.session['user']
  except KeyError:
    guest_login = None
  search = ''
  searched_products = []
  if request.method == 'POST':
    search = request.POST['product_search']
    products_by_brand = Product.objects.filter(brand=search)
    searched_products.extend(products_by_brand)
    #* Next line inspiration gotten from https://stackoverflow.com/questions/7088173/how-to-query-model-where-name-contains-any-word-in-python-list
    products_by_name = Product.objects.filter(Q(name__contains=search))
    searched_products.extend(products_by_name)
    

  context = {'searched_products': searched_products, 'search': search, 'guest_login': guest_login}
  return render(request, 'store/product_search.html', context)

# Delete Product By Admin Logic
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)
    deleted = request.session.get('deleted', 'empty')
    request.session['deleted'] = product.name
    product.delete()
    messages.success(request, product.name + ' has been deleted successfully')
    return redirect('index')


# Cart page logic
def cart(request):
  guest_login = request.session.get('user', '')
  user = request.user
  # use order and line item models if user is signed in with username
  if user.is_authenticated:
    customer = user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.lineitem_set.all()
  # if user is signed in as guest, use sessions to hold the basket
  elif guest_login == 'guest':
    items = get_basket(request)
    total_amount = 0
    total_quantity = 0
    for item in items:
      total_amount += item.get_total()
      total_quantity += item.quantity
    request.session['amount'] = str(total_amount)
    request.session['quantity'] = str(total_quantity)
    order = {'get_cart_total': total_amount, 'get_cart_items': total_quantity}
  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  context = {'items': items, 'order': order, 'guest_login': guest_login}
  return render(request, 'store/cart.html', context)

def checkout(request):
  guest_login = request.session.get('user', '')
  user = request.user
  if user.is_authenticated != True and guest_login != 'guest':
    return redirect('login')
  if user.is_authenticated:
    customer = user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 
    items = order.lineitem_set.all()
  elif guest_login == 'guest':
    items = get_basket(request)
    total_amount = request.session.get('amount', 0)
    total_quantity = request.session.get('quantity', 0)
    order = {'get_cart_total': total_amount, 'get_cart_items': total_quantity}

  else:
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
  context = {'items': items, 'order': order, 'guest_login': guest_login, 'user': user}
  return render(request, 'store/checkout.html', context)


def dashboard(request):
  user = request.user
  if user.is_authenticated and user.is_staff:
    all_brands = {}
    products = Product.objects.all()
    for product in products:
      brand = product.brand
      if brand in all_brands:
        all_brands[brand] += 1
      else:
        all_brands[brand] = 1
    all_brands = dict(sorted(all_brands.items(), key=lambda item: item[1]))
    brand_names = list(all_brands.keys())
    brand_numbers = list(all_brands.values())
    number5 = brand_numbers[-1]
    number4 = brand_numbers[-2]
    number3 = brand_numbers[-3]
    number2 = brand_numbers[-4]
    number1 = brand_numbers[-5]
    name5 = brand_names[-1]
    name4 = brand_names[-2]
    name3 = brand_names[-3]
    name2 = brand_names[-4]
    name1 = brand_names[-5] 
    orders = Order.objects.all()
    for order in orders:
      print(orders)
    brand_names = reversed(brand_names)
    brand_numbers = reversed(brand_numbers)
    context = {'names': brand_names, 'numbers': brand_numbers, 'number5':number5, 'number4':number4, 'number3':number3,
    'number2':number2, 'number1':number1, 'name5': name5, 'name4': name4, 'name3': name3, 'name2': name2, 'name1': name1,
    'orders': orders}
    return render(request, 'store/dashboard.html', context)
  else:
    return redirect('login')


# save order, clear basket and thank customer
def payment(request):
  if request.method == "POST":
    try:
      guest_login = request.session['user']
    except KeyError:
      guest_login = None
    
    user = request.user 
    if user.is_authenticated:
      customer = user.customer
      order, created = Order.objects.get_or_create(customer=customer, complete=False) 
      items = order.lineitem_set.all()

    # if user is signed in as guest, use sessions to hold the basket
    elif guest_login == 'guest':
      email = request.POST.get('email', '')
      name = request.POST.get('name', '')
      customer, created = Customer.objects.get_or_create(email=email)
      customer.name = name
      customer.save()
      order = Order.objects.create(customer=customer, complete=False)
      basket = request.session.get('basket', [])
      for item in basket:
        product = Product.objects.get(id=item[0])
        lineItem = LineItem.objects.create(product=product, order=order, quantity=item[1])
      del request.session['basket']


    # order.refresh_from_db()
    order.complete = True
    order.save()
    order.refresh_from_db()
    # if order.complete == True:
    #   ShippingAddress.objects.create(
    #     customer=customer,
    #     order=order,
    #     address=address,
    #     city=city,
    #     state=state,
    #     zipcode=zipcode
    #   )
    messages.success(request, 'Thank you for your order. It has been processed successfully')
    return redirect('index')

def contact(request):
  try:
    guest_login = request.session['user']
  except KeyError:
    guest_login = None
  return render(request, 'store/contact.html', {'guest_login': guest_login})