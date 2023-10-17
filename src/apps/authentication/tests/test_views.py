import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_login_view(user1) -> None:  # type: ignore
    client = APIClient()
    url = '/api/auth/login/'

    response = client.post(
        url,
        {
            'email': '1@1.com',
            'password': '1',
        },
        format='json'
    )

    assert response.status_code == 201
    assert 'token' in response.data


@pytest.mark.django_db
def test_register_view() -> None:
    client = APIClient()
    url = '/api/auth/register/'

    response = client.post(
        url,
        {
            'email': '1@1.com',
            'username': '1',
            'password': '1',
            'password1': '1',
        },
        format='json'
    )

    assert response.status_code == 201
    assert 'password' not in response.data

    assert response.data['username'] == '1'
    assert response.data['email'] == '1@1.com'
