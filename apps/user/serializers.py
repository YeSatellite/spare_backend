# coding=utf-8
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.user.models import User

USER_FIELDS = ('id', 'username', 'first_name', 'last_name', 'address', 'avatar', 'type', 'password', 'money')
USER_READ_ONLY_FIELDS = ('id', 'username', 'type', 'money')


class UserProfileSerializer(ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = User
        fields = USER_FIELDS
        read_only_fields = USER_READ_ONLY_FIELDS
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
