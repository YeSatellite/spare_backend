# coding=utf-8
from django.db import models

from apps.core.models import TimeStampedMixin

OK = 'ok'
FEW = 'few'
OVER = 'over'

PRODUCT_STATUS_CHOICES = (
    ('k', OK),
    ('f', FEW),
    ('o', OVER),
)


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
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=PRODUCT_STATUS_CHOICES)

    type = models.ForeignKey(ProductType, models.CASCADE)
    place = models.ForeignKey(Place, models.CASCADE, null=True)

    def __str__(self):
        return str("%s, %s" % (self.type, self.name))
