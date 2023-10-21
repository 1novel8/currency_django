from typing import Any

from django.core.exceptions import ObjectDoesNotExist

from apps.base.exceptions import NotFound
from apps.base.repositories import BaseRepository
from apps.user.models import User


class UserRepository(BaseRepository):
    model = User

    def get_by_email(self, email: str) -> User | Any:
        try:
            return self.model.objects.get(email=email)
        except ObjectDoesNotExist as exc:
            raise NotFound('User with such email not found') from exc

    def is_email_exists(self, email: str) -> bool | Any:
        return self.model.objects.filter(email=email).exists()

    def create(self, **kwargs: Any) -> Any:
        return self.model.objects.create_user(**kwargs)
