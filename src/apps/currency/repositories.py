from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from apps.base.exceptions import NotFound
from apps.base.repositories import BaseRepository
from apps.currency.models import Currency


class CurrencyRepository(BaseRepository):
    model = Currency

    def get_buy_name(self, name: str) -> Currency:
        try:
            return self.model.objects.get(name=name)
        except ObjectDoesNotExist as exc:
            raise NotFound('object not found') from exc

    @staticmethod
    def update_price(currency: Currency, price_for_buy: Decimal, price_for_sale: Decimal) -> Currency:
        currency.price_for_buy = price_for_buy
        currency.price_for_sale = price_for_sale
        currency.save(update_fields=['price_for_buy', 'price_for_sale'])
        return currency
