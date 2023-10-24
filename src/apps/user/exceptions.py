from rest_framework import status
from rest_framework.exceptions import APIException


class WalletAlreadyExists(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Wallet with such currency already exists'
