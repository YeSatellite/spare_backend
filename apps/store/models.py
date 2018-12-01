# coding=utf-8
from django.db import models

from apps.core.models import TimeStampedMixin
from apps.depot.models import Product
from apps.user.models import User

WAITING = 'w'
ACTIVE = 'a'
FINISHED = 'f'
CANCELED = 'c'

ORDER_STATUS_CHOICES = (
    (WAITING, 'waiting'),
    (ACTIVE, 'active'),
    (FINISHED, 'finished'),
    (CANCELED, 'canceled'),
)


# =============================================================


class Order(TimeStampedMixin):

    client = models.ForeignKey(User, models.CASCADE, related_name='order_client')
    registered = models.ForeignKey(User, models.CASCADE, related_name='order_registered')

    status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES)

    def __str__(self):
        return str("%s %s" % (self.client, self.created.strftime('%d-%m-%Y')))


class OrderItem(TimeStampedMixin):
    order = models.ForeignKey(Order, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    registered = models.ForeignKey(User, models.CASCADE)

    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES,
                              default=ORDER_STATUS_CHOICES[0][0])

    def total(self):
        return self.amount*self.price

    def __str__(self):
        return str("%s: %s" % (self.order, self.product))
