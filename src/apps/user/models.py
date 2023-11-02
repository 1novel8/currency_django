from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from apps.base.enums import Role
from apps.base.models import BaseModel
from apps.base.utils import upload_to
from apps.user.managers import CustomUserManager


class User(
    BaseModel,
    AbstractBaseUser,
    PermissionsMixin,
):
    username = models.CharField(
        "Username",
        max_length=50,
        blank=False,
    )
    email = models.EmailField(
        "Email Address",
        unique=True,
        blank=False,
    )
    password = models.CharField(
        "Password",
        max_length=200,
        blank=False,
    )
    role = models.CharField(
        "Role",
        max_length=10,
        blank=False,
        choices=Role.choices,
        default=Role.USER,
    )
    balance = models.DecimalField(
        "Balance",
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    currency_subscriptions = models.ManyToManyField(
        'currency.Currency',
        related_name='user_subscriptions',
    )

    image = models.ImageField(
        storage=S3Boto3Storage(),
        upload_to=upload_to,
        blank=True,
        null=True,
        default=None,
    )

    @property
    def is_staff(self) -> bool:
        return self.role == Role.ADMIN

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"


class Wallet(BaseModel):
    """ Wallet model"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        'currency.Currency',
        on_delete=models.DO_NOTHING,
    )
    balance = models.DecimalField(
        "Balance",
        max_digits=16,
        decimal_places=6,
        default=0,
    )

    def __str__(self) -> str:
        return f'wallet {self.id}: {self.currency.name} - {self.balance}'

    class Meta:
        db_table = "wallet"
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
