from functools import wraps

from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def paginate(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)
        assert isinstance(queryset, (
        list, QuerySet)), "apply_pagination expects a List or a QuerySet"

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    return inner


class CorePagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class LargePagination(CorePagination):
    """
    large pagination class.
    """

    page_size = 15


class MediumPagination(CorePagination):
    """
    medium pagination class.
    """

    page_size = 10


class SmallPagination(CorePagination):
    """
    small pagination class.
    """

    page_size = 5
