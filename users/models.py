from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    deposit = models.IntegerField(default=0)
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')

    # override the default fields
    groups = None  
    user_permissions = None

    class Meta:
        app_label = 'users'