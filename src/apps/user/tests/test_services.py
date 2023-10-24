import pytest

from apps.base.exceptions import NotFound
from apps.user.exceptions import WalletAlreadyExists
from apps.user.services import WalletService


@pytest.mark.django_db
def test_wallet_create(user1, currency_usd):
    service = WalletService()
    wallet = service.create(user=user1, currency=currency_usd)

    assert wallet.user == user1
    assert wallet.currency == currency_usd
    assert wallet.balance == 0


@pytest.mark.django_db
def test_wallet_create_failure(user1, currency_usd):
    service = WalletService()
    service.create(user=user1, currency=currency_usd)
    with pytest.raises(WalletAlreadyExists):
        service.create(user=user1, currency=currency_usd)


@pytest.mark.django_db
def test_wallet_delete(user1, currency_usd):
    service = WalletService()
    wallet = service.create(user=user1, currency=currency_usd)
    wallet.balance = 100
    balance = wallet.currency.price_for_sale * wallet.balance
    wallet.save()
    service.delete(user=user1, wallet=wallet)
    assert user1.balance == balance


@pytest.mark.django_db
def test_wallet_delete_failure(user1, currency_usd):
    service = WalletService()
    wallet = service.create(user=user1, currency=currency_usd)
    service.delete(user=user1, wallet=wallet)
    with pytest.raises(NotFound):
        service.delete(user=user1, wallet=wallet)
