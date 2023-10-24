from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.base.mixins import PermissionsByActionMixin
from apps.user.models import Wallet
from apps.user.serializers import WalletSerializer
from apps.user.services import WalletService


class WalletViewSet(
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
    }
    serializer_class = WalletSerializer
    service = WalletService()

    def get_queryset(self) -> QuerySet[Wallet]:
        user = self.request.user
        return Wallet.objects.filter(user=user).all()

    def perform_create(self, serializer: WalletSerializer) -> None:
        self.service.create(user=self.request.user, **serializer.validated_data)

    def perform_destroy(self, instance: Wallet) -> None:
        self.service.delete(user=self.request.user, wallet=instance)
