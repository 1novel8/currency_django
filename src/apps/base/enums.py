from django.db import models


class Role(models.TextChoices):
    """ User Roles"""

    ANALYST = 'Analyst'
    USER = 'User'
    ADMIN = 'Admin'


class OrderType(models.TextChoices):
    """ Types of Orders """

    BUY = 'Buy'
    SALE = 'Sale'


class OrderStatus(models.TextChoices):
    """ Status of order """

    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    CANCELED = 'Canceled'
