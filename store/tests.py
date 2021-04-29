from django.test import TestCase
from store.models import Product
# Create your tests here.

#* Reference https://docs.djangoproject.com/en/3.2/topics/testing/overview/
class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="tshirt", price=23, brand="adidas", image_url="https://image.png")
        Product.objects.create(name="socks", price=2.6, brand="nike", image_url="https://image2.png")

    def test_all_products_length(self):
        products = Product.objects.all()
        self.assertEqual(len(products), 2)

    def test_product_exists(self):
        shirt = Product.objects.get(name="tshirt")
        socks = Product.objects.get(name="socks")
        self.assertEqual(shirt.brand, 'adidas')
        self.assertEqual(socks.brand, 'nike')
