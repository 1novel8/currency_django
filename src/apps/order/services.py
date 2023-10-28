from typing import Any

from django.db.models import QuerySet
from django.utils import timezone

from apps.base.enums import OrderStatus, OrderType
from apps.base.exceptions import NotFound
from apps.base.services import BaseService
from apps.order.exceptions import OrderAlreadyFinishedException
from apps.order.models import Order
from apps.order.repositories import OrderRepository
from apps.user.models import User


class OrderService(BaseService):
    repository = OrderRepository()

    def get_orders_by_user(self, user: User) -> QuerySet[Order]:
        return self.repository.get_orders_by_user(user=user)

    def create(self, **kwargs: Any) -> Order | Any:
        wallet = kwargs['wallet']
        user = kwargs.pop('user')
        if wallet.user != user:
            raise NotFound('No such wallet')
        order = super().create(**kwargs)

        # if order.price == None -> it's quick order
        if order.price is None:
            self.check_order(order=order)
        return order

    def cancel(self, order_pk: int) -> None:
        order = self.get_by_pk(pk=order_pk)
        if order.status != OrderStatus.IN_PROGRESS:
            raise OrderAlreadyFinishedException
        order.status = OrderStatus.CANCELED
        order.finished_at = timezone.now()
        order.save()

    def check_order(self, order: Order) -> None:
        switch_check = {
            OrderType.BUY.name: self._check_buy_order,
            OrderType.SALE.name: self._check_sale_order,
        }
        switch_check[order.type](order=order)

    @staticmethod
    def _check_buy_order(order: Order) -> None:
        wallet = order.wallet
        user = wallet.user
        currency = wallet.currency

        # it's important
        # if order.price == None, it means that it's quick order
        # and its price is current price for currency right now
        if order.price is None:
            order.price = currency.price_for_buy
        elif currency.price_for_buy > order.price:
            # if price is not preferred - None
            return None

        total_price = order.price * order.count
        if user.balance < total_price:
            # if user hove not enough money - None & set finished_at now
            order.status = OrderStatus.CANCELED
            order.finished_at = timezone.now()
            order.save()
            return None

        # change user balance
        user.balance -= total_price
        user.save()
        # change wallet balance
        wallet.balance += order.count
        wallet.save()
        # finish order
        order.status = OrderStatus.DONE
        order.finished_at = timezone.now()
        order.save()

        return None

    @staticmethod
    def _check_sale_order(order: Order) -> None:
        wallet = order.wallet
        user = wallet.user
        currency = wallet.currency

        # it's important
        # if order.price == None, it means that it's quick order
        # and its price is current price for currency right now
        if order.price is None:
            order.price = currency.price_for_sale
        elif currency.price_for_sale < order.price:
            # if price is not preferred - None
            return None

        if wallet.balance < order.count:
            # if user have not enough currency - None & set finished_at now
            order.status = OrderStatus.CANCELED
            order.finished_at = timezone.now()
            order.save()
            return None

        total_price = order.price * order.count
        # change wallet balance
        wallet.balance -= order.count
        wallet.save()
        # change user balance
        user.balance += total_price
        user.save()
        # finish order
        order.status = OrderStatus.DONE
        order.finished_at = timezone.now()
        order.save()

        return None
