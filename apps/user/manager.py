# coding=utf-8
from django.contrib.auth.base_user import BaseUserManager

ADMIN = 'a'
STAFF = 's'
CLIENT = 'c'
GUEST = 'g'

USER_TYPE_CHOICES = (
    (ADMIN, 'admin'),
    (STAFF, 'staff'),
    (CLIENT, 'client'),
    (GUEST, 'guest'),
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, first_name, last_name, password, **extra_fields):
        user = self.model(username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, first_name, last_name, password, **extra_fields):
        return self._create_user(username, first_name, last_name, password, **extra_fields)

    def create_superuser(self, username, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('type', ADMIN)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, first_name, last_name, password, **extra_fields)


class ClientManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=CLIENT)

