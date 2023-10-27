from typing import Any

from django.contrib.auth.base_user import BaseUserManager

from apps.base.enums import Role


class CustomUserManager(
    BaseUserManager,  # type: ignore
):
    """ Manager for user Model """

    def create_user(   # type: ignore
            self,
            username: str,
            email: str, password: str,
            role: str = Role.USER,
            is_superuser: bool = False,
            **extra_fields: dict[str, Any]
    ):

        if email is None:
            raise ValueError('Users must have an email address.')
        if password is None:
            raise ValueError('Users must have an password.')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str):  # type: ignore
        user = self.create_user(
            username='admin',
            email=email,
            password=password,
            role=Role.ADMIN,
            is_superuser=True,
        )
        return user
