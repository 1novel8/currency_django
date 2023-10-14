from enum import Enum


class Role(Enum):
    """ User Roles"""

    ANALYST = 'Analyst'
    USER = 'User'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.name, choice.value) for choice in cls]


class OrderType(Enum):
    """ Types of Orders """

    BUY = 'Buy'
    SALE = 'Sale'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.name, choice.value) for choice in cls]


class OrderStatus(Enum):
    """ Status of order """

    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    CANCELED = 'Canceled'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.name, choice.value) for choice in cls]
