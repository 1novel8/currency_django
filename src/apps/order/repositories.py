from django.db.models import QuerySet

from apps.base.enums import OrderStatus
from apps.base.repositories import BaseRepository
from apps.order.models import Order
from apps.user.models import User


class OrderRepository(BaseRepository):
    model = Order

    def get_orders_by_user(self, queryset: QuerySet[Order],  user: User | None) -> QuerySet[Order]:
        if not user:
            return queryset
        return queryset.filter(wallet__user=user).all()

    def get_orders_in_progress(self, queryset: QuerySet[Order]) -> QuerySet[Order]:
        return queryset.filter(status=OrderStatus.IN_PROGRESS).all()
