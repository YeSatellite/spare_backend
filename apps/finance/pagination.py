from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TradePagination(PageNumberPagination):
    page_size = 8
    max_page_size = 1000

    def get_page_size(self, request):
        if request.query_params.get('client', None):
            return self.max_page_size

        return self.page_size

    def get_paginated_response(self, data):
        return Response({
            'pages': self.page.paginator.num_pages,
            'results': data
        })
