from rest_framework import status
from rest_framework.exceptions import APIException


class OrderAlreadyFinishedException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'You can not cancel already finished order'
