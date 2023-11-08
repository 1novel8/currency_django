from typing import Any

from apps.base.repositories import BaseRepository


class BaseService:
    repository = BaseRepository()

    def get_all(self) -> Any:
        return self.repository.get_all()

    def get_by_pk(self, pk: int) -> Any:  # pylint: disable=invalid-name
        return self.repository.get_by_pk(pk=pk)

    def create(self, **kwargs: Any) -> Any:
        return self.repository.create(**kwargs)
