from typing import Any

from django.contrib.auth import get_user_model
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication

from apps.authentication.exceptions import InvalidHeader, InvalidToken, TokenExpired
from apps.authentication.services import AuthenticationService
from apps.user.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: HttpRequest) -> None | tuple[User, Any]:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            if not token.startswith('Bearer '):
                raise InvalidHeader

            token = token.split(' ')[1]
            payload = AuthenticationService.decode_jwt(token=token)
            user = get_user_model().objects.get(id=payload['id'])
            return (user, None)

        except (TokenExpired, InvalidToken, InvalidHeader):
            return None
