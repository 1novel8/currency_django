from typing import Any

from apps.authentication.exceptions import EmailAlreadyExists
from apps.base.services import BaseService
from apps.user.models import User
from apps.user.repositories import UserRepository


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
