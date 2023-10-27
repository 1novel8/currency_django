from typing import Any

from django.db.models import QuerySet
from django.utils import timezone

from apps.base.enums import OrderStatus
from apps.base.exceptions import NotFound
from apps.base.services import BaseService
from apps.order.exceptions import OrderAlreadyFinishedException
from apps.order.models import Order
from apps.order.repositories import OrderRepository
from apps.user.models import User


class OrderService(BaseService):
    repository = OrderRepository()

    def get_queryset(self, user: User) -> QuerySet[Order]:
        return self.repository.get_queryset(user=user)

    def create(self, **kwargs: Any) -> Order | Any:
        wallet = kwargs['wallet']
        user = kwargs.pop('user')
        if wallet.user != user:
            raise NotFound('No such wallet')
        return super().create(**kwargs)

    def cancel(self, order_pk: int) -> None:
        order = self.get_by_pk(pk=order_pk)
        if order.status != OrderStatus.IN_PROGRESS:
            raise OrderAlreadyFinishedException
        order.status = OrderStatus.CANCELED
        order.finished_at = timezone.now()
        order.save()
