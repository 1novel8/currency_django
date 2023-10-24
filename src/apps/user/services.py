from typing import Any

from apps.authentication.exceptions import EmailAlreadyExists
from apps.base.exceptions import NotFound
from apps.base.services import BaseService
from apps.currency.models import Currency
from apps.user.exceptions import WalletAlreadyExists
from apps.user.models import User, Wallet
from apps.user.repositories import UserRepository, WalletRepository


class UserService(BaseService):
    repository = UserRepository()

    def is_email_exists(self, email: str) -> bool | Any:
        return self.repository.is_email_exists(email=email)

    def get_by_email(self, email: str) -> User | Any:
        return self.repository.get_by_email(email=email)

    def create(self, email: str, username: str, password: str) -> User | Any:  # type: ignore
        if self.is_email_exists(email=email):
            raise EmailAlreadyExists()

        user = super().create(
            email=email,
            username=username,
            password=password,
        )
        return user


class WalletService(BaseService):
    repository = WalletRepository()

    def create(self, **kwargs: Any) -> Wallet | Any:
        currency = kwargs['currency']
        user = kwargs['user']
        if self.is_exist(user=user, currency=currency):
            raise WalletAlreadyExists
        return super().create(**kwargs)

    def is_exist(self, user: User, currency: Currency) -> bool:
        return self.repository.is_exist(user=user, currency=currency)

    def delete(self, user: User, wallet: Wallet) -> None:
        if not self.is_exist(user=user, currency=wallet.currency):
            raise NotFound('User have no such wallet')
        self.repository.delete(user=user, wallet=wallet)
