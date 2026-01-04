from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum, unique
from typing import TypedDict
from uuid import UUID

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import Pagination, ToDictMixin


@unique
class OrderStatus(StrEnum):
    CREATED = "created"
    CHANGED = "changed"
    DELIVERED = "delivered"
    TO_CANCEL = "to_cancel"
    CANCELLED = "cancelled"
    PAID = "paid"


class OrderProduct(TypedDict):
    name: str
    quantity: int


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrderAsUser(ToDictMixin):
    user_id: UUID
    pickup_address_name: str
    status: OrderStatus
    delivered_at: date
    has_delivery: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrder(ToDictMixin):
    user_id: UUID
    pickup_address_name: str
    status: OrderStatus
    products: Sequence[OrderProduct]
    delivered_at: date
    price: int


@dataclass(frozen=True, kw_only=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    pickup_address_name: str
    status: OrderStatus
    products: Sequence[Mapping]
    delivered_at: date
    price: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderListParams(Pagination):
    user_id: UUID | None = None
    pickup_address_name: str | None = None
    statuses: Sequence[OrderStatus] | None = None
    delivered_at: date | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderList:
    total: int
    items: Sequence[Order]


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateOrder(ToDictMixin):
    id: UUID
    user_id: UUID | Unset = UNSET
    pickup_address_name: str | Unset = UNSET
    status: OrderStatus | Unset = UNSET
    products: Sequence[OrderProduct] | Unset = UNSET
    delivered_at: date | Unset = UNSET
    price: int | Unset = UNSET
