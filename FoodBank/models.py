from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, unique=True)
    pan = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username


class CorpInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, unique=True)
    pan = models.CharField(max_length=10, unique=True)
    tan = models.CharField(max_length=10, unique=True)
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.name


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username
