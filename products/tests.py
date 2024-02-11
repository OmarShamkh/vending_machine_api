from django.test import TestCase
from .models import Product
from users.models import CustomUser

class ProductTestCase(TestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create_user(username='seller', password='password123', role='seller')
        self.product_data = {
            'productName': 'Test Product',
            'amountAvailable': 10,
            'cost': 5.00,
            'sellerId': self.seller
        }
        self.product = Product.objects.create(**self.product_data)

    def test_product_creation(self):
        # Test if a product was created successfully
        self.assertEqual(self.product.productName, self.product_data['productName'])
        self.assertEqual(self.product.amountAvailable, self.product_data['amountAvailable'])
        self.assertEqual(self.product.cost, self.product_data['cost'])
        self.assertEqual(self.product.sellerId, self.product_data['sellerId'])

    def test_product_update(self):
        # Test if a product can be updated successfully
        new_product_data = {
            'productName': 'Updated Product',
            'amountAvailable': 20,
            'cost': 10.00,
            'sellerId': self.seller
        }
        self.product.productName = new_product_data['productName']
        self.product.amountAvailable = new_product_data['amountAvailable']
        self.product.cost = new_product_data['cost']
        self.product.save()
        self.product.refresh_from_db()
        self.assertEqual(self.product.productName, new_product_data['productName'])
        self.assertEqual(self.product.amountAvailable, new_product_data['amountAvailable'])
        self.assertEqual(self.product.cost, new_product_data['cost'])

    def test_product_deletion(self):
        # Test if a product can be deleted successfully
        product_id = self.product.id
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)

