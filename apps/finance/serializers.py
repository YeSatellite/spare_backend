# coding=utf-8
from django.db import transaction
from django.db.models import Sum, F
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from apps.core.serializers import MyChoiceField
from apps.finance.models import Trade, GOOD, MONEY
from apps.store.models import ACTIVE, Order
from apps.store.serializers import OrderSerializer
from apps.user.manager import USER_TYPE_CHOICES
from apps.user.models import User
from apps.user.serializers import UserProfileSerializer


class TradeSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True, required=False)
    order = OrderSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)

    def validate(self, attrs):
        print(attrs['type'])
        if attrs['type'] == GOOD:
            attrs['client'] = Order.objects.get(id=attrs['order_id']).client
            attrs['money'] = 0
        if attrs['type'] == MONEY:
            attrs['order_id'] = None
        attrs['registered'] = self.context['request'].user
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        trade = super().create(validated_data)  # type: Trade

        if trade.type == GOOD:
            order = trade.order
            order.status = ACTIVE
            order.save()

            items = order.orderitem_set
            if items.filter(status=False).count() != 0:
                raise ParseError({'order_id': ['Order has waiting items']})

            money = items.filter(status=True).aggregate(money=Sum(F('amount') * F('price')))['money']
            money = money if money else 0
            trade.money = money
            money = -trade.money
        else:
            money = trade.money

        client = trade.client
        trades = Trade.objects.filter(client=client).order_by('-created')
        last_trade = trades[1 if trades.count() > 1 else 0]

        if last_trade.sum != client.money:
            pass  # TODO

        client.money += money
        client.save()

        trade.sum = last_trade.sum + money
        trade.save()

        return trade

    class Meta:
        model = Trade
        fields = ('id', 'order_id', 'order', 'registered', 'type', 'money', 'sum', 'created', 'client')
        read_only_fields = ('id', 'registered', 'sum')


USER_FIELDS = ('id', 'username', 'first_name', 'last_name', 'address', 'avatar', 'type', 'money')


class ClientSerializer(serializers.ModelSerializer):
    type = MyChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = USER_FIELDS
