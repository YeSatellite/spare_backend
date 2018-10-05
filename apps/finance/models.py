# coding=utf-8

from django.db import models

from apps.core.models import TimeStampedMixin
from apps.depot.models import Product
from apps.store.models import Order
from apps.user.models import User

IN = 'i'
OUT = 'o'

TRADE_TYPE_CHOICES = (
    (IN, 'in'),
    (OUT, 'out'),
)


class Trade(TimeStampedMixin):
    order = models.OneToOneField(Order, models.CASCADE, null=True)
    registered = models.ForeignKey(User, models.CASCADE)
    money = models.PositiveIntegerField()

    type = models.CharField(max_length=1, choices=TRADE_TYPE_CHOICES)

    def __str__(self):
        return str("%s /%s" % (self.order, self.created.strftime('%d-%m-%Y')))
