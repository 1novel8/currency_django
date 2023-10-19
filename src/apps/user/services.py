from typing import Any

from django.core.exceptions import ObjectDoesNotExist

from apps.authentication.exceptions import EmailAlreadyExists
from apps.base.exceptions import NotFound
from apps.user.models import User


class UserService:
    model = User

    def is_email_exists(self, email: str) -> bool | Any:
        return self.model.objects.filter(email=email).exists()

    def get_user_by_email(self, email: str) -> User | Any:
        try:
            return self.model.objects.get(email=email)
        except ObjectDoesNotExist as exc:
            raise NotFound('User with such email not found') from exc

    def create(self, email: str, username: str, password: str) -> User | Any:
        if self.is_email_exists(email=email):
            raise EmailAlreadyExists()

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        return user
