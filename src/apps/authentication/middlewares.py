from typing import Any, Callable

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest

from apps.authentication.exceptions import InvalidHeader, InvalidToken, TokenExpired
from apps.authentication.services import AuthenticationService


class JWTMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], Any]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        try:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            if not token.startswith(f'{settings.JWT.get("HEADER")} '):
                raise InvalidHeader()

            token = token.split(' ')[1]
            payload = AuthenticationService.decode_jwt(token=token)
            user = get_user_model().objects.get(id=payload['id'])
            request.user = user
            login(request, user)

        except (TokenExpired, InvalidToken, InvalidHeader):
            request.user = AnonymousUser()

        finally:
            response = self.get_response(request)

        return response  # response
