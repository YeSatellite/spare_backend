# coding=utf-8

from django.db import models

from apps.core.models import TimeStampedMixin
from apps.depot.models import Product
from apps.store.models import Order
from apps.user.models import User

IN = 'g'
OUT = 'm'

TRADE_TYPE_CHOICES = (
    (IN, 'good'),
    (OUT, 'money'),
)


class Trade(TimeStampedMixin):
    order = models.OneToOneField(Order, models.CASCADE, null=True)
    registered = models.ForeignKey(User, models.CASCADE)
    type = models.CharField(max_length=1, choices=TRADE_TYPE_CHOICES)

    money = models.PositiveIntegerField(default=0)
    sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str("%s /%s" % (self.order, self.created.strftime('%d-%m-%Y')))
