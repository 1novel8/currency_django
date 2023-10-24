from rest_framework import status
from rest_framework.exceptions import APIException


class FinishedOrderException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You can not delete already finished order'
