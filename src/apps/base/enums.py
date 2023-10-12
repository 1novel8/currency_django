from enum import Enum


class Role(Enum):
    ANALYST = 'Analyst'
    USER = 'User'
    ADMIN = 'Admin'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class OrderType(Enum):
    BUY = 'Buy'
    SALE = 'Sale'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class OrderStatus(Enum):
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    CANCELED = 'Canceled'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
