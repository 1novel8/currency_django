from django.db.models import QuerySet

from apps.base.repositories import BaseRepository
from apps.order.models import Order
from apps.user.models import User


class OrderRepository(BaseRepository):
    model = Order

    @staticmethod
    def get_queryset(user: User | None) -> QuerySet[Order]:
        if user:
            return Order.objects.filter(wallet__user=user).all()
        return Order.objects.all()
