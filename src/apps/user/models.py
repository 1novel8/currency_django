from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.base.enums import Role
from apps.base.models import BaseModel
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
        choices=Role.choices(),
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

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"


class Wallet(BaseModel):
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

    class Meta:
        db_table = "wallet"
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
