from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class TradePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'pages': self.page.paginator.num_pages,
            'results': data
        })
