# coding=utf-8
from django.contrib import admin

from apps.depot.models import Device, ProductType, Product, Place

admin.site.register(Device)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Place)
