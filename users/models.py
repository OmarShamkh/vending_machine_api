from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    deposit = models.IntegerField(default=0)
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    # Provide unique related_name arguments for groups and user_permissions fields
    groups = None  # Remove default related_name
    user_permissions = None  # Remove default related_name

    class Meta:
        # Specify a unique app_label for your custom User model
        app_label = 'users'