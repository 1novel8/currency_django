from typing import Any

from apps.base.enums import OrderStatus
from apps.base.exceptions import NotFound
from apps.base.services import BaseService
from apps.order.exceptions import FinishedOrderException
from apps.order.models import Order
from apps.order.repositories import OrderRepository


class OrderService(BaseService):
    repository = OrderRepository()

    def create(self, **kwargs: Any) -> Order | Any:
        wallet = kwargs['wallet']
        user = kwargs['user']
        if wallet.user != user:
            raise NotFound('No such wallet')
        return super().create(**kwargs)

    def delete(self, order: Order) -> None:
        if order.status != OrderStatus.IN_PROGRESS.name:
            raise FinishedOrderException
        order.delete()
