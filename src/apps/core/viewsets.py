"""
core viewsets module.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from apps.core.utilities import make_iterable


class CoreViewSet(viewsets.GenericViewSet):
    """
    core view set class.

    every view set must be subclassed from this.
    """

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = '__all__'
    queryset = None
    serializer_class = None
    permission_classes = None
    pagination_class = None

    querysets = {}
    serializers = {}
    permissions = {}

    pagination_classes = {}

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            pagination_class = self.pagination_classes.get(
                self.action,
                self.pagination_class
            )
            self._paginator = None

            if callable(pagination_class):
                self._paginator = pagination_class()

            if isinstance(pagination_class, dict):
                pagination_class = pagination_class.get(
                    self.request.method.lower(), self.pagination_class)

                if callable(pagination_class):
                    self._paginator = pagination_class()

        return self._paginator

    def get_serializer_class(self):
        """
        gets the related serializer to the current method.

        it returns the default `serializer_class` if the method has no
        custom serializer.
        """

        serializer = self.serializers.get(self.action, self.serializer_class)
        if isinstance(serializer, dict):
            return serializer.get(self.request.method.lower(),
                                  self.serializer_class)

        return serializer

    def get_permissions(self):
        """
        gets the related permissions to the current method.

        it uses the default `permission_classes` if the method has no
        custom permission.
        """

        result = self.permissions.get(self.action, self.permission_classes)
        result = make_iterable(result)
        return [permission() for permission in result]
