# coding=utf-8
from rest_framework.routers import DefaultRouter

from apps.depot.views import DeviceViewSet, ProductTypeViewSet, ProductViewSet, PlaceViewSet

router = DefaultRouter()
router.register(r'places', PlaceViewSet, base_name='place')
router.register(r'devices', DeviceViewSet, base_name='device')
router.register(r'product-type', ProductTypeViewSet, base_name='product-type')
router.register(r'product', ProductViewSet, base_name='product')


urlpatterns = router.urls
urlpatterns += []

