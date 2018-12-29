# coding=utf-8

import logging
from django.conf import settings
from rest_framework import exceptions
from rest_framework.views import exception_handler

norm = logging.getLogger('project.need').debug


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    error_code = getattr(settings, 'ERROR_CODE', None)
    assert isinstance(error_code, dict)
    if isinstance(exc, exceptions.APIException):
        if isinstance(exc.detail, dict):
            r_error_code = 100
            for key, value in error_code.items():
                if isinstance(key, str):
                    field = key
                    message = None
                elif isinstance(key, (list, tuple)):
                    assert len(key) == 2
                    assert isinstance(key[0], str)
                    assert isinstance(key[1], str)
                    field = key[0]
                    message = key[1]
                else:
                    raise AssertionError('key error')

                exc_message = exc.detail.get(field, None)
                if not exc_message:
                    continue

                if message is None or (message in exc_message):
                    r_error_code = value
                    break
            response['Error-Code'] = r_error_code

    return response


def digit3(n, end=' ₸'):
    n = str(n)
    t = len(n) // 3
    r = len(n) - t * 3
    s = n[0:r]
    for i in range(t):
        s = s + ' ' + n[r + 3 * i:r + 3 * (i + 1)]
    return s + end
