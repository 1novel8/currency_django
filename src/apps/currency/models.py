from django.db import models

from apps.base.models import BaseModel


class Currency(BaseModel):
    name = models.CharField(
        "Name",
        max_length=50,
        blank=False,
    )
    price_for_buy = models.DecimalField(
        "Price for buy",
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    price_for_sale = models.DecimalField(
        "Price for buy",
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "currency"
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
