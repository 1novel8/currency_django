from django.db.models import QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.base.enums import Role
from apps.base.mixins import PermissionsByActionMixin, SerializeByActionMixin
from apps.base.permissions import IsOrderInProgress
from apps.order.models import Order
from apps.order.serializers import OrderCancelSerializer, OrderSerializer
from apps.order.services import OrderService


class OrderViewSet(
    PermissionsByActionMixin,
    SerializeByActionMixin,
    UpdateModelMixin,
    GenericViewSet,
    RetrieveModelMixin,
    ListModelMixin,
):
    serialize_by_action = {
        'cancel': OrderCancelSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]
    permissions_by_action = {
        'update': [IsOrderInProgress, permissions.IsAuthenticated],
        'partial_update': [IsOrderInProgress, permissions.IsAuthenticated],
        'cancel': [IsOrderInProgress, permissions.IsAuthenticated],
    }
    serializer_class = OrderSerializer
    service = OrderService()

    def get_queryset(self) -> QuerySet[Order]:
        queryset = self.service.get_all()
        if self.request.user.role == Role.USER:
            queryset = self.service.get_orders_by_user(queryset=queryset, user=self.request.user)
        return queryset  # type: ignore

    @action(detail=True, methods=['post'])
    def cancel(self, request: Request, pk: str) -> Response:
        self.service.cancel(order_pk=int(pk))
        return Response(status=status.HTTP_200_OK)

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.service.create(user=self.request.user, **serializer.validated_data)
        serializer = self.get_serializer(instance=order)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
