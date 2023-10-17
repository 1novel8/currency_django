from rest_framework import status
from rest_framework.exceptions import APIException


class EmailAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Email already in use'


class BadCredentials(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'User with such email and password is not exist'


class TokenExpired(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token expired'


class InvalidToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid token'


class InvalidHeader(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid token'
