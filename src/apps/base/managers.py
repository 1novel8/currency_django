from django.db.models import Manager
from django.utils import timezone


class BaseModelManager(Manager):
    """
    Base Manager for models inherited from BaseModel.

    get_queryset() - returns objects with field 'deleted_at == True'.
    all() - returns objects with field 'deleted_at == True'.
    delete() - soft delete.
    """

    def _get_queryset(self):
        """ default queryset """
        return super().get_queryset()

    def get_queryset(self):
        """ filtered queryset """

        queryset = self._get_queryset()
        queryset = queryset.filter(deleted_at__isnull=True)
        return queryset

    def all_fully(self):
        """ default .all() """
        return self._get_queryset()

    def all(self):
        """ filtered .all() """
        return self.get_queryset()

    def delete(self):
        """ soft delete for multiple instances """
        self.update(delete_at=timezone.now())
