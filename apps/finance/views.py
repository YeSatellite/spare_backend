# coding=utf-8
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.finance.models import Trade
from apps.finance.serializers import TradeSerializer, ClientSerializer
from apps.user.models import User
from apps.user.permission import UserIsAdmin


class TradeViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = TradeSerializer
    queryset = Trade.objects.all()


class ClientViewSet(ReadOnlyModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = ClientSerializer
    queryset = User.clients.all()
