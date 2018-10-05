# coding=utf-8
from rest_framework.routers import DefaultRouter

from apps.finance.views import TradeViewSet, ClientViewSet
from apps.store.views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'trades', TradeViewSet, base_name='trade')
router.register(r'clients', ClientViewSet, base_name='client')
urlpatterns = router.urls
urlpatterns += []

