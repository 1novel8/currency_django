from typing import Any

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request

from apps.base.enums import OrderStatus, Role


class IsOwnerOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:  # pylint: disable=unused-argument
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user in (obj, Role.ADMIN)


class IsOrderInProgress(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:  # pylint: disable=unused-argument
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.status == OrderStatus.IN_PROGRESS  # type: ignore
