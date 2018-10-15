# coding=utf-8
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from apps.core.serializers import MyChoiceField
from apps.finance.models import TRADE_TYPE_CHOICES, Trade
from apps.store.models import ACTIVE, WAITING
from apps.store.serializers import OrderSerializer
from apps.user.models import User
from apps.user.serializers import UserProfileSerializer


class TradeSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(write_only=True)
    order = OrderSerializer(read_only=True)

    registered = UserProfileSerializer(read_only=True)

    status = MyChoiceField(choices=TRADE_TYPE_CHOICES)

    def validate(self, attrs):
        attrs['registered'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        obj = super().create(validated_data)  # type: Trade
        order = obj.order
        client = order.client
        items = order.orderitem_set
        if items.filter(status=WAITING).count() != 0:
            raise ParseError({'order_id': ['Order has waiting items']})

        money = items.filter(status=ACTIVE).aggregate(money=Sum('total'))['money']

        order.status = ACTIVE
        order.save()

        client.money -= money
        return obj

    class Meta:
        model = Trade
        fields = ('id', 'order_id', 'order', 'registered', 'status')
        read_only_fields = ('id', 'registered')


USER_FIELDS = ('id', 'username', 'first_name', 'last_name', 'address', 'avatar', 'type', 'money')


class ClientSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = User
        fields = USER_FIELDS