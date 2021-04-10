from django.db import models
from django.contrib.auth.models import User

# create models here

class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=True)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200, null=True)
  created_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user},{self.name},{self.created_date}'


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField() 
    image_url = models.CharField(max_length=200,null=True)
    brand = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name},{self.price},{self.created_date}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transation_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.customer},{self.created_date}'


class LineItem(models.Model):
    quantity = models.IntegerField(default=0, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product.name},{self.order.customer.name},{self.created_date}'

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.address