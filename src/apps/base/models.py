from django.db import models


class BaseModel(models.Model):
    """
    Base Model for inheritance for solid instances.
    Implements some additional fields.
    Overrides default manager "objects".
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, )

    class Meta:
        abstract = True
