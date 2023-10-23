from apps.base.repositories import BaseRepository
from apps.currency.models import Currency


class CurrencyRepository(BaseRepository):
    model = Currency
