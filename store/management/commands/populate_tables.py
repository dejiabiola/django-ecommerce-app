"""
This file will populate the tables using Faker
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

from store.models import ShippingAddress, Customer, LineItem, Order, Product

class Command(BaseCommand):
    help = 'Load data into the tables'

    def handle(self, *args, **options):

        # drop the tables - use this order due to foreign keys - so that we can rerun the file as needed without repeating values
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
        ShippingAddress.objects.all().delete()
        print("tables dropped successfully")

        # fake = Faker()

        # # create some products
        # for i in range(10):
        #     product = Product.objects.create(
        #     name = fake.catch_phrase(),
        #     price = int( decimal.Decimal(random.randrange(155,899))/100),
        #     )
        #     product.save()

        # create the table
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        with open(str(base_dir) + '/store/csv_folder/mens_westernwear.csv', newline='') as f:
          reader = csv.reader(f, delimiter=",")
          next(reader)
          for row in reader:
            print(row)
            product = Product.objects.create(
              name = row[0],
              price = float(row[1]),
              brand = row[5],
              image_url = row[6]
            )
            product.save()

        
        print("tables successfully loaded")
               
    
