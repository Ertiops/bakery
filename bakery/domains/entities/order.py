from enum import StrEnum, unique
from typing import TypedDict
from uuid import UUID


@unique
class OrderStatus(StrEnum):
    ON_ACCEPT = "on_accept"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    PAID = "paid"


class OrderProduct(TypedDict):
    product_id: UUID
    quantity: int
