# coding=utf-8
from django.conf.urls import url

from apps.user.views import UserProfileAPIView, login

urlpatterns = [
    url(r'profile/', UserProfileAPIView.as_view()),
    url(r'login/', login),
]
