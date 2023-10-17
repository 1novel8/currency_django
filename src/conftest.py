import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user1(db):
    user = get_user_model().objects.create_user(
        email='1@1.com',
        password='1',
        username='1',
    )
    return user
