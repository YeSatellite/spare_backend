# coding=utf-8
from rest_framework.routers import DefaultRouter

from apps.store.views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, base_name='order')
router.register(r'order-items', OrderItemViewSet, base_name='order-item')
urlpatterns = router.urls
urlpatterns += []

