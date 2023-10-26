from celery import shared_task
from django.utils import timezone

from apps.base.enums import OrderStatus, OrderType
from apps.order.models import Order


@shared_task(queue='periodic')
def check_orders() -> None:
    check_order = {
        OrderType.BUY.name: check_buy_order,
        OrderType.SALE.name: check_sale_order,
    }
    orders_in_progress = (Order.objects
                          .filter(status=OrderStatus.IN_PROGRESS.name)
                          .select_related('wallet__currency', 'wallet__user').all())
    for order in orders_in_progress:
        check_order[order.type](order=order)


def check_buy_order(order: Order) -> None:
    wallet = order.wallet
    user = wallet.user
    currency = wallet.currency
    if currency.price_for_buy > order.price:
        # if price is not preferred - None
        return None

    total_price = order.price * order.count
    if user.balance < total_price:
        # if user hove not enough money - None & set finished_at now
        order.status = OrderStatus.CANCELED.name
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
    order.status = OrderStatus.DONE.name
    order.finished_at = timezone.now()
    order.save()

    return None


def check_sale_order(order: Order) -> None:
    wallet = order.wallet
    user = wallet.user
    currency = wallet.currency
    if currency.price_for_sale < order.price:
        # if price is not preferred - None
        return None

    if wallet.balance < order.count:
        # if user have not enough currency - None & set finished_at now
        order.status = OrderStatus.CANCELED.name
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
    order.status = OrderStatus.DONE.name
    order.finished_at = timezone.now()
    order.save()

    return None
