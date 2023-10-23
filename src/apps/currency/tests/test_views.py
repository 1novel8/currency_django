import pytest
from conftest import get_auth_header
from django.urls import reverse
from rest_framework.test import APIClient

currency_raw = {
    'name': 'usd',
    'price_for_buy': 1,
    'price_for_sale': 20.2
}

currency_invalid_raw = {
    'name': 'usd',
    'price_for_buy': 1.1234,
    'price_for_sale': 20.223
}

currency_for_update = {
    'name': 'dsu',
    'price_for_buy': 132,
    'price_for_sale': 202.5
}


@pytest.mark.django_db
def test_currency_create(admin_user) -> None:  # type: ignore
    client = APIClient()
    url = reverse('currency-list')
    auth_header = get_auth_header(email=admin_user.email, password='admin')

    response = client.post(
        url,
        currency_raw,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 400
    assert response.data['name'] == currency_raw['name']
    assert float(response.data['price_for_buy']) == float(currency_raw['price_for_buy'])
    assert float(response.data['price_for_sale']) == float(currency_raw['price_for_sale'])


@pytest.mark.django_db
def test_currency_create_failure(admin_user) -> None:  # type: ignore
    client = APIClient()
    url = reverse('currency-list')
    auth_header = get_auth_header(email=admin_user.email, password='admin')

    response = client.post(
        url,
        currency_invalid_raw,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_currency_create_access_denied(user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse('currency-list')
    auth_header = get_auth_header(email=user1.email, password='1')

    response = client.post(
        url,
        currency_raw,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 403

    response = client.post(
        url,
        currency_raw,
        format='json'
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_currency_list(user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse('currency-list')
    auth_header = get_auth_header(email=user1.email, password='1')

    response = client.get(
        url,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_currency_list_access_denied() -> None:  # type: ignore
    client = APIClient()
    url = reverse('currency-list')

    response = client.get(
        url,
        format='json'
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_currency_retrieve(currency_usd, user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=user1.email,  password='1')

    response = client.get(
        url,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_currency_retrieve_access_denied(currency_usd) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])

    response = client.get(
        url,
        format='json'
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_currency_put(currency_usd, admin_user) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=admin_user.email, password='admin')

    response = client.put(
        url,
        currency_for_update,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_currency_put_access_denied(currency_usd, user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=user1.email, password='1')

    response = client.put(
        url,
        currency_for_update,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_currency_patch(currency_usd, admin_user) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=admin_user.email, password='admin')

    response = client.patch(
        url,
        {'name': currency_for_update['name']},
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_currency_patch_access_denied(currency_usd, user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=user1.email, password='1')

    response = client.patch(
        url,
        {'name': currency_for_update['name']},
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_currency_delete(currency_usd, admin_user) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=admin_user.email, password='admin')

    response = client.delete(
        url,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 204
    assert response.data is None


@pytest.mark.django_db
def test_currency_delete_access_denied(currency_usd, user1) -> None:  # type: ignore
    client = APIClient()
    url = reverse("currency-detail", args=[currency_usd.id])
    auth_header = get_auth_header(email=user1.email, password='1')

    response = client.delete(
        url,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 403

    response = client.get(
        url,
        headers=auth_header,
        format='json'
    )
    assert response.status_code == 200
