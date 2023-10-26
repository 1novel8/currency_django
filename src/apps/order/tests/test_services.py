import pytest

from apps.base.enums import OrderStatus, OrderType
from apps.order.exceptions import OrderAlreadyFinishedException
from apps.order.services import OrderService

raw_order_buy = {
    'type': OrderType.BUY.name,
    'price': 12,
    'count': 12,
}


@pytest.mark.django_db
def test_order_create(user1, currency_usd, wallet_usd_user1):
    service = OrderService()
    order = service.create(user=user1, wallet=wallet_usd_user1, **raw_order_buy)

    assert order.status == OrderStatus.IN_PROGRESS.name
    assert order.type == raw_order_buy['type']
    assert order.price == raw_order_buy['price']
    assert order.count == raw_order_buy['count']
    assert order.wallet == wallet_usd_user1


@pytest.mark.django_db
def test_order_cancel(order_wallet_usd_user1):
    service = OrderService()
    service.cancel(order_pk=order_wallet_usd_user1.id)
    order = service.get_by_pk(pk=order_wallet_usd_user1.id)
    assert order.status == OrderStatus.CANCELED.name
    assert order.finished_at is not None


@pytest.mark.django_db
def test_order_cancel_failure(order_wallet_usd_user1):
    service = OrderService()
    service.cancel(order_pk=order_wallet_usd_user1.id)

    with pytest.raises(OrderAlreadyFinishedException):
        service.cancel(order_pk=order_wallet_usd_user1.id)
