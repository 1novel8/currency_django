from typing import Type

from rest_framework.permissions import BasePermission
from rest_framework.serializers import Serializer


class SerializeByActionMixin:
    serialize_by_action: dict[str, Type[Serializer]]
    action: str

    def get_serializer_class(self) -> Type[Serializer]:
        try:
            return self.serialize_by_action[self.action]
        except KeyError:
            return super().get_serializer_class()  # type: ignore


class PermissionsByActionMixin:
    permissions_by_action: dict[str, list[Type[BasePermission]]]
    action: str

    def get_permissions(self) -> list[BasePermission]:
        try:
            permission_classes = self.permissions_by_action[self.action]
            return [permission() for permission in permission_classes]
        except KeyError:
            return super().get_permissions()  # type: ignore
