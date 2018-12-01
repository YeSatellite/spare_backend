# coding=utf-8

import jwt
from django.conf import settings
from django.contrib.auth.models import update_last_login, Group, Permission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_payload_handler

from apps.user.serializers import UserProfileSerializer
from .models import User


class UserProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = UserProfileSerializer

    def get_object(self, queryset=None):
        return self.request.user


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise AuthenticationFailed({'username': ["Username doesn't exist"]})
    if not user.check_password(password):
        raise AuthenticationFailed({'password': ["Invalid password"]})

    user.sms_code = None
    user.save()
    serializer = UserProfileSerializer(user, context={"request": request})
    data = serializer.data

    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    update_last_login(None, user)
    data['token'] = token.decode('unicode_escape')

    return Response(data)
