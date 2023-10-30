from django.db.models import QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.base.mixins import PermissionsByActionMixin, SerializeByActionMixin
from apps.order.serializers import OrderSerializer
from apps.user.models import Wallet
from apps.user.serializers import WalletSerializer
from apps.user.services import WalletService


class WalletViewSet(
    SerializeByActionMixin,
    PermissionsByActionMixin,
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
):
    permissions_by_action = {
        'create': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
        'list': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated],
        'history': [permissions.IsAuthenticated],
    }
    serialize_by_action = {
        'history': OrderSerializer,
    }
    serializer_class = WalletSerializer
    service = WalletService()

    def get_queryset(self) -> QuerySet[Wallet]:
        queryset = self.service.get_wallets_by_user(user=self.request.user)
        return queryset

    def perform_create(self, serializer: WalletSerializer) -> None:
        self.service.create(user=self.request.user, **serializer.validated_data)

    def perform_destroy(self, instance: Wallet) -> None:
        self.service.delete(user=self.request.user, wallet=instance)

    @action(detail=True, methods=['get'])
    def history(self, request: Request, pk: int) -> Response:  # pylint: disable=invalid-name, unused-argument
        orders = self.service.get_wallet_orders(pk=pk)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
