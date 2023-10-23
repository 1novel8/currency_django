from rest_framework import exceptions, status


class UserAlreadySubscribedException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User already subscribed on this currency'


class UserHaveNoSubscriptionException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User is not subscribed on this currency'
