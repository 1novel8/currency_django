from django.contrib.auth.base_user import BaseUserManager

from apps.base.enums import Role
from apps.base.managers import BaseModelManager


class CustomUserManager(
    BaseUserManager,
    BaseModelManager,
):
    def create_user(self, username, email, password, **extra_fields):
        if email is None:
            raise ValueError('Users must have an email address.')
        if password is None:
            raise ValueError('Users must have an password.')

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password)
        user.is_superuser = True
        user.role = Role.ADMIN
        user.save()
        return user
