from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from apps.base.exceptions import NotFound
from apps.base.repositories import BaseRepository
from apps.currency.models import Currency
from apps.user.models import User, Wallet


class UserRepository(BaseRepository):
    model = User

    def get_by_email(self, email: str) -> User | Any:
        try:
            return self.model.objects.get(email=email)
        except ObjectDoesNotExist as exc:
            raise NotFound('User with such email not found') from exc

    def is_email_exists(self, email: str) -> bool | Any:
        return self.model.objects.filter(email=email).exists()

    def create(self, **kwargs: Any) -> Any:
        return self.model.objects.create_user(**kwargs)


class WalletRepository(BaseRepository):
    model = Wallet

    @staticmethod
    def get_wallets_by_user(user: User | None) -> QuerySet[Wallet]:
        if user:
            return Wallet.objects.filter(user=user).all()
        return Wallet.objects.all()

    def is_exist(self, user: User, currency: Currency) -> bool:
        return self.model.objects.filter(user=user, currency=currency).exists()

    @staticmethod
    def delete(user: User, wallet: Wallet) -> None:
        price_for_sale = wallet.currency.price_for_sale
        money_back = wallet.balance * price_for_sale

        user.balance += money_back
        user.save(update_fields=('balance', ))
        wallet.delete()
