"""
This file will populate the tables using the CSV file
"""
import csv
import os
import random
import decimal
from datetime import datetime
from django.db import models
from pathlib import Path
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from store.models import Customer, LineItem, Order, Product

class Command(BaseCommand):
    help = 'Load data into the tables'

    def handle(self, *args, **options):

        # drop the tables - use this order due to foreign keys - so that we can rerun the file as needed without repeating values
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
        print("tables dropped successfully")

        fake = Faker()

        # create some customers
        #! Add links to where code was copied
        for i in range(10):
          first_name = fake.first_name(),
          last_name = fake.last_name(),
          username = first_name + last_name,
          user = User.objects.create_user(
          username = username,
          first_name = first_name,
          last_name = last_name,
          email = fake.ascii_free_email(), 
          password = 'p@ssw0rd')
          customer = Customer.objects.get(user = user)
          customer.address = fake.address(),
          customer.save()

        # read products from 
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/store/csv_folder/mens_westernwear.csv', newline='') as f:
          reader = csv.reader(f, delimiter=",")
          next(reader)
          for row in reader:
            print(row)
            product = Product.objects.create(
              name = row[0].lower(),
              price = float(row[1]),
              brand = row[5].lower(),
              image_url = row[6]
            )
            product.save()

        
        print("tables successfully loaded")
               
    
