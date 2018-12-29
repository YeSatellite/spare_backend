# coding=utf-8
from django.db.models import Sum, F, Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.serializers import MyChoiceField, time_stamp_fields, id_fields
from apps.depot.serializers import ProductSerializer
from apps.store.models import Order, OrderItem, ORDER_STATUS_CHOICES
from apps.user.manager import CLIENT
from apps.user.models import User
from apps.user.serializers import UserProfileSerializer


def is_client(user):
    if User.objects.get(id=user).type != CLIENT:
        raise ValidationError({'client': ["Only client"]})
    return user


class OrderSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True, validators=[is_client])
    client = UserProfileSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)
    items_info = serializers.SerializerMethodField()

    def get_items_info(self, obj):
        items = obj.orderitem_set

        info = items.filter(status=True).aggregate(
            money=Sum(F('amount') * F('price')),
            count=Count('amount'))
        infoAll = items.aggregate(
            money=Sum(F('amount') * F('price')),
            count=Count('amount'))

        return {
            'money': info['money'] if info['money'] else 0,
            'count': info['count'] if info['count'] else 0,
            'moneyAll': infoAll['money'] if infoAll['money'] else 0,
            'countAll': infoAll['count'] if infoAll['count'] else 0,
        }

    def validate(self, attrs):
        attrs['registered'] = self.context['request'].user
        return attrs

    class Meta:
        model = Order
        fields = id_fields + ('client_id', 'client', 'registered', 'status', 'items_info') + time_stamp_fields
        read_only_fields = ('registered', 'status',) + id_fields


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)

    def validate(self, attrs):
        attrs['registered'] = self.context['request'].user
        return attrs

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product_id', 'product', 'registered', 'amount', 'price', 'status')
        read_only_fields = ('id', 'registered')
