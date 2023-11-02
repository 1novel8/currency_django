from django.db.models import QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.base.enums import Role
from apps.base.mixins import PermissionsByActionMixin, SerializeByActionMixin
from apps.base.permissions import IsOwnerOrAdminUser
from apps.order.serializers import OrderSerializer
from apps.user.models import User, Wallet
from apps.user.serializers import ChangeRoleSerializer, TopUpBalanceSerializer, UserSerializer, WalletSerializer
from apps.user.services import UserService, WalletService


class UserViewSet(
    SerializeByActionMixin,
    PermissionsByActionMixin,
    GenericViewSet,
    RetrieveModelMixin,
    ListModelMixin,
):
    permissions_by_action = {
        'list': [permissions.IsAuthenticated],
        'retrieve': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated, permissions.IsAdminUser],
        'top_up_balance': [permissions.IsAuthenticated, IsOwnerOrAdminUser],
        'change_role': [permissions.IsAdminUser],
    }
    serializer_class = UserSerializer
    serialize_by_action = {
        'top_up_balance': TopUpBalanceSerializer,
        'change_role': ChangeRoleSerializer,
    }
    service = UserService()

    def get_queryset(self) -> QuerySet[User]:
        queryset = self.service.get_all()
        if not self.request.user.is_authenticated:
            return queryset  # type: ignore
        if self.request.user.role in (Role.ADMIN, Role.ANALYST):
            return queryset  # type: ignore
        if self.request.user.role == Role.USER:
            queryset = queryset.filter(email=self.request.user.email)
        return queryset  # type: ignore

    @action(detail=True, methods=['post'])
    def top_up_balance(self, request: Request, pk: int) -> Response:  # pylint: disable=invalid-name, unused-argument
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = self.get_object()
        self.service.top_up_balance(user=user, count=serializer.validated_data['count'])

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def change_role(self, request: Request, pk: int) -> Response:  # pylint: disable=invalid-name, unused-argument
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = self.get_object()
        self.service.change_role(user=user, role=serializer.validated_data['role'])

        return Response(status=status.HTTP_201_CREATED)


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
        if not self.request.user.is_authenticated:
            return self.service.get_all()  # type: ignore
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
