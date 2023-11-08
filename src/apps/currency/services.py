from decimal import Decimal
from typing import Any

from django.core.exceptions import ObjectDoesNotExist

from apps.base.services import BaseService
from apps.currency.exceptions import UserAlreadySubscribedException, UserHaveNoSubscriptionException
from apps.currency.models import Currency
from apps.currency.repositories import CurrencyRepository
from apps.user.models import User


class CurrencyService(BaseService):
    repository = CurrencyRepository()

    def subscribe(self, user: User, currency_pk: int) -> Any:
        subscription = self.get_subscription(user=user, currency_pk=currency_pk)
        if subscription:
            raise UserAlreadySubscribedException

        currency = self.get_by_pk(pk=currency_pk)
        user.currency_subscriptions.add(currency)

    def unsubscribe(self, user: User, currency_pk: int) -> Any:
        subscription = self.get_subscription(user=user, currency_pk=currency_pk)
        if subscription is None:
            raise UserHaveNoSubscriptionException

        subscription.delete()

    @staticmethod
    def get_subscription(user: User, currency_pk: int) -> Any:
        try:
            subscription = user.currency_subscriptions.through.objects.get(  # type: ignore
                currency_id=currency_pk,
                user_id=user.id
            )
            return subscription
        except ObjectDoesNotExist:
            return None

    def get_buy_name(self, name: str) -> Currency:
        return self.repository.get_buy_name(name=name)

    def update_price(self, name: str, price_for_sale: Decimal, price_for_buy: Decimal) -> Currency:
        currency = self.get_buy_name(name=name)
        currency = self.repository.update_price(
            currency=currency,
            price_for_sale=price_for_sale,
            price_for_buy=price_for_buy
        )
        return currency
