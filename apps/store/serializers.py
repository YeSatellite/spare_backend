# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.serializers import MyChoiceField
from apps.depot.serializers import ProductSerializer
from apps.store.models import Order, OrderItem, ORDER_STATUS_CHOICES
from apps.user.manager import CLIENT
from apps.user.models import User
from apps.user.serializers import UserProfileSerializer


def is_client(user):
    if User.objects.get(id=user).get_type_display() != CLIENT:
        raise ValidationError({'client': ["Only client"]})
    return user


class OrderSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField(write_only=True, validators=[is_client])
    client = UserProfileSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)

    status = MyChoiceField(choices=ORDER_STATUS_CHOICES)

    def validate(self, attrs):
        attrs['registered'] = self.context['request'].user
        return attrs

    class Meta:
        model = Order
        fields = ('id', 'client_id', 'client', 'registered', 'status')
        read_only_fields = ('id', 'registered')


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)

    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)

    status = MyChoiceField(choices=ORDER_STATUS_CHOICES)

    def validate(self, attrs):
        attrs['registered'] = self.context['request'].user
        return attrs

    class Meta:
        model = OrderItem
        fields = ('id', 'order_id', 'product_id', 'product', 'registered', 'amount', 'price', 'status')
        read_only_fields = ('id', 'registered')
