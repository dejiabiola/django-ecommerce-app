from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save

# create models here
# Code Referenced
# https://github.com/divanov11/django_ecommerce_mod5/blob/master/store/models.py
# https://github.com/scharlau/shopping_exercise_django/blob/main/shop/models.py
class Customer(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=200, null=True)
  email = models.CharField(max_length=200)
  address = models.TextField(null=True)
  created_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user},{self.name},{self.created_date}'

  class Meta:
    db_table = 'customer'

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
        Customer.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()

class User(models.Model):
  name = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2) 
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

    @property
    def get_cart_total(self):
      lineitems = self.lineitem_set.all()
      total = 0
      for item in lineitems:
        total += item.get_total
      return total

    @property
    def get_cart_items(self):
      lineitems = self.lineitem_set.all()
      total = 0
      for item in lineitems:
        total += item.quantity
      return total

    def __str__(self):
      return f'{self.customer},{self.created_date}'



class LineItem(models.Model):
    quantity = models.IntegerField(default=0, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return f'{self.quantity},{self.product.name},{self.order.customer.name},{self.created_date}'

    @property
    def get_total(self):
      total = self.product.price * self.quantity
      return total
