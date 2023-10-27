import pytest
from django.contrib.auth import get_user_model

from apps.authentication.services import AuthenticationService
from apps.base.enums import OrderType
from apps.currency.models import Currency
from apps.order.models import Order
from apps.user.models import User, Wallet


@pytest.fixture
def user1(db):
    user = get_user_model().objects.create_user(
        email='1@1.com',
        password='1',
        username='1',
    )
    yield user


@pytest.fixture
def admin_user(db):
    admin = get_user_model().objects.create_superuser(
        email='admin@admin.com',
        password='admin',
    )
    return admin


@pytest.fixture
def currency_usd(db):
    currency = Currency.objects.create(
        name='usd',
        price_for_buy=1,
        price_for_sale=20.2,
    )
    return currency


@pytest.fixture
def wallet_usd_user1(currency_usd: Currency, user1: User):
    wallet = Wallet.objects.create(
        user=user1,
        currency=currency_usd,
    )
    yield wallet


@pytest.fixture
def order_wallet_usd_user1(wallet_usd_user1):
    order = Order.objects.create(
        type=OrderType.BUY.value,
        price=12,
        count=12,
        wallet=wallet_usd_user1,
    )
    return order


def get_auth_header(email, password):
    auth_header = {
        'Authorization': 'Bearer ' + AuthenticationService.generate_jwt(
            email=email,
            password=password,
        )
    }
    return auth_header
