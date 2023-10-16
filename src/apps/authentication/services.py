from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model

from apps.authentication.exceptions import BadCredentials, EmailAlreadyInUse, InvalidToken, TokenExpired

User = get_user_model()


class AuthenticationService:
    def create_user(self, email: str, username: str, password: str) -> None:
        if self.is_email_exists(email=email):
            raise EmailAlreadyInUse()

        User.objects.create_user(
            email=email,
            username=username,
            password=password
        )

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

    @staticmethod
    def is_email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()
