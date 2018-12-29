# coding=utf-8
from django.db import models

from apps.core.models import TimeStampedMixin


# =============================================================

class Place(TimeStampedMixin):
    name = models.CharField(max_length=10, unique=True)
    definition = models.CharField(max_length=100)

    def __str__(self):
        return str("%s" % self.name)


# =============================================================

class Device(TimeStampedMixin):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class ProductType(TimeStampedMixin):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, models.CASCADE)

    def __str__(self):
        return str(self.name)


class Product(TimeStampedMixin):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', null=True)
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=2)

    type = models.ForeignKey(ProductType, models.CASCADE)
    place = models.ForeignKey(Place, models.CASCADE, null=True)

    def __str__(self):
        return str("%s, %s" % (self.type, self.name))
