from django.contrib import admin
from .models import UserInfo, Product, Donation, CorpInfo

# Register your models here.

admin.site.register([UserInfo, Product, Donation, CorpInfo])
