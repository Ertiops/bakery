from enum import StrEnum, unique


@unique
class OrderStatus(StrEnum):
    ON_ACCEPT = "on_accept"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    PAID = "paid"
