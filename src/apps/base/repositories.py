from typing import Any, Type

from django.core.exceptions import ObjectDoesNotExist

from apps.base.exceptions import NotFound
from apps.base.models import BaseModel


class BaseRepository:
    model: Type[BaseModel]

    def create(self, **kwargs: Any) -> Any:
        obj = self.model.objects.create(**kwargs)  # type: ignore
        return obj

    def get_by_pk(self, pk: int) -> Any:  # pylint: disable=invalid-name
        try:
            obj = self.model.objects.get(id=pk)  # type: ignore
            return obj
        except ObjectDoesNotExist as exc:
            raise NotFound('object not found') from exc

    def get_all(self) -> Any:
        return self.model.objects.all()  # type: ignore
