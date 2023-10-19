from django.db import models

from apps.base.enums import OrderStatus, OrderType
from apps.base.models import BaseModel


class Order(BaseModel):
    count = models.DecimalField(
        "Count",
        max_digits=12,
        decimal_places=6,
        default=0,
        blank=False,
    )
    price = models.DecimalField(
        "Price",
        max_digits=12,
        decimal_places=6,
        default=0,
        blank=False,
    )
    type = models.CharField(
        "Type",
        max_length=10,
        blank=False,
        choices=OrderType.choices(),
        default=OrderType.BUY,
    )
    finished_at = models.DateTimeField(
        "Finished at",
        default=None,
        null=True,
    )
    status = models.CharField(
        "Status",
        max_length=15,
        blank=False,
        choices=OrderStatus.choices(),
        default=OrderStatus.IN_PROGRESS,
    )
    wallet = models.ForeignKey(
        'user.Wallet',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
