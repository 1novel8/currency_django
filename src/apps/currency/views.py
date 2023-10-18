from rest_framework import permissions
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from apps.base.mixins import PermissionsByActionMixin
from apps.currency.models import Currency
from apps.currency.serializers import CurrencySerializer


class CurrencyViewSet(
    PermissionsByActionMixin,
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
):
    """ ViewSet for Currency """

    permissions_by_action = {
        'create': [permissions.IsAdminUser],
        'retrieve': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAdminUser],
        'partial_update': [permissions.IsAdminUser],
        'list': [permissions.IsAuthenticated],
        'update': [permissions.IsAdminUser],
    }
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()
