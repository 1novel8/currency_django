from enum import StrEnum


class Role(StrEnum):
    """ User Roles"""

    ANALYST = 'Analyst'
    USER = 'User'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.value, choice.value) for choice in cls]


class OrderType(StrEnum):
    """ Types of Orders """

    BUY = 'Buy'
    SALE = 'Sale'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.value, choice.value) for choice in cls]


class OrderStatus(StrEnum):
    """ Status of order """

    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    CANCELED = 'Canceled'

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(choice.value, choice.value) for choice in cls]
