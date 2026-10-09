"""
ExamForge M2 — Custom Pagination Classes
==========================================
Provides consistent, configurable pagination across all M2 endpoints.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    """
    Standard pagination for general list endpoints.
    Supports custom page size via query parameter.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'pagination': {
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.get_page_size(self.request),
            },
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'status': {'type': 'string', 'example': 'success'},
                'pagination': {
                    'type': 'object',
                    'properties': {
                        'count': {'type': 'integer', 'example': 123},
                        'total_pages': {'type': 'integer', 'example': 7},
                        'current_page': {'type': 'integer', 'example': 1},
                        'next': {'type': 'string', 'nullable': True},
                        'previous': {'type': 'string', 'nullable': True},
                        'page_size': {'type': 'integer', 'example': 20},
                    },
                },
                'results': schema,
            },
        }


class LargeResultsPagination(PageNumberPagination):
    """
    Larger pagination for bulk export or report endpoints.
    """
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'pagination': {
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.get_page_size(self.request),
            },
            'results': data,
        })


class SmallResultsPagination(PageNumberPagination):
    """
    Smaller pagination for dropdown-style list endpoints.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'status': 'success',
            'pagination': {
                'count': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.get_page_size(self.request),
            },
            'results': data,
        })


StandardPagination = StandardResultsPagination
