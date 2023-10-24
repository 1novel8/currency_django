from apps.base.repositories import BaseRepository
from apps.order.models import Order


class OrderRepository(BaseRepository):
    model = Order
