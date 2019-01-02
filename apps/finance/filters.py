# coding=utf-8
from django.db.models import Q
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
        if 'search' in pars:
            searches = pars['search'].split()
            for search in searches:
                queryset = queryset.filter(
                    Q(order__client__username__startswith=search) |
                    Q(order__client__first_name__startswith=search) |
                    Q(order__client__last_name__startswith=search))
        if 'archive' in pars:
            status = 'f' if pars['archive'] in TRUE else 'a'
            queryset = queryset.filter(order__status=status)

        return queryset
