# coding=utf-8
from django.contrib import admin

from apps.store.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
