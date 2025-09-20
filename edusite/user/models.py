
from django.db import models

from product.models import Product


# Create your models here.
class Register(models.Model):
    user_email = models.EmailField(null=True)
    user_phone = models.CharField(max_length=15,null=True)
    code = models.PositiveIntegerField()
    date_register=models.DateField(null=True)

    def __str__(self):
        return self.user_email

class Users(models.Model):
    user_name = models.CharField(max_length=100, unique=True)
    user_email = models.CharField(max_length=150, unique=True)
    user_phone = models.CharField(max_length=15, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user_email

class Purchases(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.user_email