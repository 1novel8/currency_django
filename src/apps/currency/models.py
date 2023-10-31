from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from apps.base.models import BaseModel
from apps.base.utils import upload_to


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
    image = models.ImageField(
        storage=S3Boto3Storage(),
        upload_to=upload_to,
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = "currency"
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
