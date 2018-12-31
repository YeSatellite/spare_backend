# coding=utf-8
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.finance.filters import TradeFilterBackend
from apps.finance.models import Trade
from apps.finance.pagination import TradePagination
from apps.finance.serializers import TradeSerializer, ClientSerializer
from apps.store.models import FINISHED
from apps.user.models import User
from apps.user.permission import UserIsAdmin


class TradeViewSet(ReadOnlyModelViewSet, CreateModelMixin):
    permission_classes = (UserIsAdmin,)
    serializer_class = TradeSerializer
    queryset = Trade.objects.all().order_by('-created')
    pagination_class = TradePagination
    filter_backends = [TradeFilterBackend, ]

    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        order = self.get_object().order
        order.status = FINISHED
        order.save()
        return self.retrieve(request)


class ClientViewSet(ReadOnlyModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = ClientSerializer
    queryset = User.clients.all()
