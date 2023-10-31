from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth import authenticate

from apps.authentication.exceptions import BadCredentials, InvalidToken, TokenExpired, WrongPassword, WrongUsername
from apps.authentication.tasks import send_new_password
from apps.user.models import User
from apps.user.services import UserService


class AuthenticationService:
    user_service = UserService()

    def create_user(self, email: str, username: str, password: str, image: str | None = None) -> User:
        user = self.user_service.create(
            email=email,
            password=password,
            username=username,
            image=image
        )
        return user

    def reset_password(self, email: str, username: str) -> None:
        user = self.user_service.get_by_email(email=email)
        if user.username != username:
            raise WrongUsername

        new_password = User.objects.make_random_password()
        user.set_password(new_password)
        send_new_password.delay(
            email=email,
            new_password=new_password,
        )
        user.save()

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> None:
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
        else:
            raise WrongPassword

    @classmethod
    def generate_jwt(cls, email: str, password: str) -> str:
        user = authenticate(username=email, password=password)
        if user is None:
            raise BadCredentials()

        token_expire = settings.JWT.get('TOKEN_EXPIRE', timedelta(days=1))
        secret_key = settings.SECRET_KEY

        payload = {
            'id': user.id,  # type: ignore
            'email': user.email,  # type: ignore
            'role': user.role,  # type: ignore
            'expired': (datetime.now() + token_expire).timestamp()
        }

        token: str = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @classmethod
    def decode_jwt(cls, token: str) -> dict[str, Any]:
        try:
            secret_key = settings.SECRET_KEY
            payload: dict[str, Any] = jwt.decode(token, secret_key, algorithms=['HS256'])
            exp_time = datetime.fromtimestamp(payload['expired'])
            if exp_time < datetime.now():
                raise TokenExpired()
            return payload
        except jwt.DecodeError as exc:
            raise InvalidToken() from exc
