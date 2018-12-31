# coding=utf-8
from rest_framework import filters

from apps.finance.models import Trade

TRUE = ['True', 'T', 'true', 't', 'Yes', 'Y', 'yes', 'y']


class TradeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        :param view:
        :type request:
        :type queryset: Trade.objects
        """
        pars = {}
        for k, v in request.query_params.items():
            if v != '':
                pars[k] = v[0]
        if 'client' in pars:
            queryset = queryset.filter(order__client=pars['client'])

        if 'archive' in pars:
            status = 'f' if pars['archive'] in TRUE else 'a'
            queryset = queryset.filter(order__status=status)

        return queryset
