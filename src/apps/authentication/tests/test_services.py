import pytest

from apps.authentication.exceptions import BadCredentials, EmailAlreadyExists, InvalidToken
from apps.authentication.services import AuthenticationService

raw_user = {
    'email': 'a@a.com',
    'username': 'a',
    'password': 'a',
    }


@pytest.mark.django_db
def test_create_user():
    service = AuthenticationService()
    user = service.create_user(**raw_user)

    assert user.email == raw_user['email']
    assert user.username == raw_user['username']
    assert user.password != raw_user['password']
    assert user.check_password(raw_user['password']) is True
    assert service.is_email_exists(raw_user['email']) is True


@pytest.mark.django_db
def test_create_user_failure(user1):  # noqa: F811
    service = AuthenticationService()
    service.create_user(**raw_user)

    with pytest.raises(EmailAlreadyExists):
        service.create_user(**raw_user)


@pytest.mark.django_db
def test_generate_jwt(user1):  # noqa: F811
    service = AuthenticationService()
    token = service.generate_jwt(email=user1.email, password='1')

    assert token is not None


@pytest.mark.django_db
def test_generate_jwt_failure():
    service = AuthenticationService()

    with pytest.raises(BadCredentials):
        service.generate_jwt(email=raw_user['email'], password=raw_user['password'])


@pytest.mark.django_db
def test_decode_jwt(user1):  # noqa: F811
    service = AuthenticationService()
    token = service.generate_jwt(email=user1.email, password='1')
    payload = service.decode_jwt(token=token)
    assert payload['id'] == user1.id
    assert payload['email'] == user1.email
    assert payload['role'] == user1.role


@pytest.mark.django_db
def test_decode_jwt_failure(user1):  # noqa: F811
    service = AuthenticationService()
    with pytest.raises(InvalidToken):
        service.decode_jwt(token='124')


@pytest.mark.django_db
def test_is_email_exist(user1):  # noqa: F811
    service = AuthenticationService()
    assert service.is_email_exists(user1.email) is True


@pytest.mark.django_db
def test_is_email_exist_failure():
    service = AuthenticationService()
    assert service.is_email_exists(raw_user['email']) is False
