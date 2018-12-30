# coding=utf-8
from django.db import transaction
from django.db.models import Sum, F
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from apps.core.serializers import MyChoiceField
from apps.finance.models import TRADE_TYPE_CHOICES, Trade
from apps.store.models import ACTIVE, WAITING, FINISHED
from apps.store.serializers import OrderSerializer
from apps.user.manager import USER_TYPE_CHOICES
from apps.user.models import User
from apps.user.serializers import UserProfileSerializer


class TradeSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    order = OrderSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)

    def validate(self, attrs):
        attrs['registered'] = self.context['request'].user
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        trade = super().create(validated_data)  # type: Trade

        order = trade.order
        order.status = ACTIVE
        order.save()

        client = order.client
        items = order.orderitem_set
        if items.filter(status=False).count() != 0:
            raise ParseError({'order_id': ['Order has waiting items']})

        money = items.filter(status=True).aggregate(money=Sum(F('amount')*F('price')))['money']
        money = money if money else 0

        client.money -= money
        client.save()

        trade.money = money
        trade.sum = trade.sum+money
        trade.save()

        return trade

    class Meta:
        model = Trade
        fields = ('id', 'order_id', 'order', 'registered', 'type', 'money', 'sum', 'created')
        read_only_fields = ('id', 'registered', 'money', 'sum')


USER_FIELDS = ('id', 'username', 'first_name', 'last_name', 'address', 'avatar', 'type', 'money')


class ClientSerializer(serializers.ModelSerializer):
    type = MyChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = USER_FIELDS
