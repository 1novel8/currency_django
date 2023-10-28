from celery import shared_task

from apps.base.enums import OrderStatus
from apps.order.models import Order
from apps.order.services import OrderService


@shared_task(queue='orders')
def check_orders() -> None:
    order_service = OrderService()
    orders_in_progress = (Order.objects
                          .filter(status=OrderStatus.IN_PROGRESS)
                          .select_related('wallet__currency', 'wallet__user').all())
    for order in orders_in_progress:
        order_service.check_order(order=order)
