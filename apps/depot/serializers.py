# coding=utf-8
from rest_framework import serializers

from apps.depot.models import Place, Device, ProductType, Product


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'name',)
        read_only_fields = ('id',)


# ================================================ #

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name')


class ProductTypeSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    device_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductType
        fields = ('id', 'name', 'device', 'device_id')


class ProductSerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer(read_only=True)
    type_id = serializers.IntegerField(write_only=True)

    place = ProductTypeSerializer(read_only=True)
    place_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'image', 'price', 'amount', 'type', 'type_id', 'place', 'place_id')
