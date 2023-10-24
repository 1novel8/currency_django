from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from apps.order.models import Order
from apps.order.serializers import OrderSerializer
from apps.order.services import OrderService


class OrderViewSet(
    GenericViewSet,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    service = OrderService()

    def get_queryset(self) -> QuerySet[Order]:
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(wallet__user=user).all()
        return Order.objects.all()

    def perform_create(self, serializer: OrderSerializer) -> None:
        self.service.create(user=self.request.user, **serializer.validated_data)

    def perform_destroy(self, instance: Order) -> None:
        self.service.delete(order=instance)
