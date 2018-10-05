# coding=utf-8
from django.contrib import admin

from apps.depot.models import Device, ProductType, Product

admin.site.register(Device)
admin.site.register(ProductType)
admin.site.register(Product)
