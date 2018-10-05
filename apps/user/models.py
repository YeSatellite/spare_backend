# coding=utf-8

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.core.models import TimeStampedMixin
from apps.user.manager import UserManager, USER_TYPE_CHOICES


class User(AbstractBaseUser,
           PermissionsMixin,
           TimeStampedMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    address = models.CharField(max_length=100, default='home')
    money = models.IntegerField(default=0)

    avatar = models.ImageField(upload_to='avatars/', null=True)

    is_staff = models.BooleanField(default=False)  # for admin page
    type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        full_name = '%s (%s %s)' % (self.username, self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.username
