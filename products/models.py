from django.db import models
from users.models import CustomUser

class Product(models.Model):
    productName = models.CharField(max_length=100)
    amountAvailable = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    sellerId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.productName
