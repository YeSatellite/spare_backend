# coding=utf-8
from .base import *

ALLOWED_HOSTS += ['192.168.1.37', '127.0.0.1', 'localhost']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p_gnmp4v*+qks+rj)1d=(7v9-exb_e5vz41#l@-*etw4rtbzf('

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': str(BASE_DIR / 'db.sqlite3'),
}

DEBUG = True
