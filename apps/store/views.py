# coding=utf-8
from rest_framework.viewsets import ModelViewSet

from apps.store.models import Order, OrderItem
from apps.store.serializers import OrderSerializer, OrderItemSerializer
from apps.user.permission import UserIsAdmin


class OrderViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
