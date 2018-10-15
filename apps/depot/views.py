# coding=utf-8
from rest_framework.viewsets import ModelViewSet

from apps.depot import filters
from apps.depot.models import Device, ProductType, Product, Place
from apps.depot.serializers import DeviceSerializer, ProductTypeSerializer, PlaceSerializer, ProductSerializer
from apps.user.permission import UserIsAdmin


class PlaceViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()


# ===================================================== #

class DeviceViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()


class ProductTypeViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = ProductTypeSerializer
    queryset = ProductType.objects.all()


class ProductViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.ProductFilterBackend,)
