from django.db import models
from django.utils import timezone

from apps.base.managers import BaseModelManager


class BaseModel(models.Model):
    """
    Base Model for inheritance for solid instances.
    Implements some additional fields and soft delete.
    Overrides default manager "objects".
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, )
    deleted_at = models.DateTimeField(default=None, null=True)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):  # pylint: disable=unused-argument
        """ soft delete for one instance """

        self.deleted_at = timezone.now()
        self.save()
