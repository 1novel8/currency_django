import pytest
from django.contrib.auth import get_user_model

from apps.authentication.services import AuthenticationService
from apps.currency.models import Currency


@pytest.fixture
def user1(db):
    user = get_user_model().objects.create_user(
        email='1@1.com',
        password='1',
        username='1',
    )
    return user


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


def get_auth_header(email, password):
    auth_header = {
        'Authorization': 'Bearer ' + AuthenticationService.generate_jwt(
            email=email,
            password=password,
        )
    }
    return auth_header
