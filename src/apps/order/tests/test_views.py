import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.base.enums import OrderType


@pytest.mark.django_db
def test_order_create(user1, wallet_usd_user1) -> None:  # type: ignore
    client = APIClient()
    client.force_authenticate(user=user1)
    url = reverse('order-list')

    response = client.post(
        url,
        {
            'type': OrderType.BUY.name,
            'price': 12,
            'count': 12,
            'wallet': wallet_usd_user1.id
        },
        format='json'
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_order_create_failure(wallet_usd_user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse('order-list')

    response = client.post(
        url,
        {
            'type': OrderType.BUY.name,
            'price': 12,
            'count': 12,
            'wallet': wallet_usd_user1.id
        },
        format='json'
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_order_cancel(user1, order_wallet_usd_user1) -> None:  # type: ignore
    client = APIClient()
    client.force_authenticate(user=user1)
    url = reverse('order-cancel', kwargs={'pk': order_wallet_usd_user1.id})

    response = client.post(
        url,
        format='json'
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_order_cancel_failure(user1, order_wallet_usd_user1) -> None:  # type: ignore
    client = APIClient()
    client.force_authenticate(user=user1)
    url = reverse('order-cancel', kwargs={'pk': order_wallet_usd_user1.id})

    client.post(
        url,
        format='json'
    )
    response = client.post(
        url,
        format='json'
    )

    assert response.status_code == 400
