from django.test import TestCase
from .models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'password123',
            'deposit': 50.00, 
            'role': 'buyer'
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_user_creation(self):
        # Test if a user was created successfully
        self.assertEqual(self.user.username, self.user_data['username'])
        self.assertTrue(self.user.check_password(self.user_data['password']))
        self.assertEqual(self.user.deposit, self.user_data['deposit'])
        self.assertEqual(self.user.role, self.user_data['role'])

    def test_deposit_increment(self):
        # Test if the deposit increases correctly
        initial_deposit = self.user.deposit
        deposit_amount = 20.00
        self.user.deposit += deposit_amount
        self.user.save()
        self.assertEqual(self.user.deposit, initial_deposit + deposit_amount)

    def test_buy_product(self):
        # Test if the deposit decreases correctly
        initial_deposit = self.user.deposit
        product_cost = 20.00
        self.user.deposit -= product_cost
        self.user.save()
        self.assertEqual(self.user.deposit, initial_deposit - product_cost)

        
    def test_reset_deposit(self):
        # Test if the deposit resets to 0
        self.user.deposit = 0
        self.user.save()
        self.assertEqual(self.user.deposit, 0)



