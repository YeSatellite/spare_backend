# coding=utf-8
from django.db.models import Q
from rest_framework import filters

from apps.depot.models import Product


class ProductFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        :param view:
        :type request:
        :type queryset: Product.objects
        """
        par = request.query_params

        devices = par.get('device', None)
        if devices:
            devices = devices.split('-')
            queryset = queryset.filter(type__device_id__in=devices)

        few = par.get('few', '0')
        if few and few == '1':
            queryset = queryset.filter(status__lte=1)

        searches = par.get('search', None)
        if searches:
            searches = [search.strip() for search in searches.split(',')]
            tmp = Product.objects.all()
            for search in searches:
                tmp = tmp.intersection(
                    queryset.filter(Q(name__contains=search) | Q(type__name__contains=search))
                )

            queryset = tmp

        return queryset
