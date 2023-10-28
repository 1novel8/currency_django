from django.db.models import QuerySet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.base.mixins import SerializeByActionMixin
from apps.order.models import Order
from apps.order.serializers import OrderCancelSerializer, OrderSerializer, QuickOrderSerializer
from apps.order.services import OrderService


class OrderViewSet(
    SerializeByActionMixin,
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    serialize_by_action = {
        'cancel': OrderCancelSerializer,
        'quick_order': QuickOrderSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    service = OrderService()

    def get_queryset(self) -> QuerySet[Order]:
        queryset = self.service.get_orders_by_user(user=self.request.user)
        return queryset

    def perform_create(self, serializer: OrderSerializer) -> None:
        self.service.create(user=self.request.user, **serializer.validated_data)

    @action(detail=True, methods=['post'])
    def cancel(self, request: Request, pk: str) -> Response:  # pylint: disable=invalid-name, unused-argument
        self.service.cancel(order_pk=int(pk))
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def quick_order(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.service.create(user=self.request.user, **serializer.validated_data)
        serializer = self.get_serializer(instance=order)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
