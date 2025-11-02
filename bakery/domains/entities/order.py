from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum, unique
from typing import TypedDict
from uuid import UUID

from bakery.application.entities import UNSET, Unset
from bakery.domains.entities.common import Pagination, ToDictMixin
from bakery.domains.entities.pickup_address import PickupAddress


@unique
class OrderStatus(StrEnum):
    ON_ACCEPT = "on_accept"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    PAID = "paid"


class OrderProduct(TypedDict):
    name: str
    quantity: int


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrder(ToDictMixin):
    user_id: UUID
    pickup_address_id: UUID | None
    status: OrderStatus
    products: Sequence[OrderProduct]
    address: str | None
    delivered_at: date
    price: int


@dataclass(frozen=True, kw_only=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    pickup_address_id: UUID
    status: OrderStatus
    products: Sequence[Mapping]
    address: str | None
    delivered_at: date
    price: int
    pickup_address: PickupAddress | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderListParams(Pagination):
    user_id: UUID | None = None
    pickup_address_id: UUID | None = None
    status: OrderStatus | None = None
    delivered_at: date | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderList:
    total: int
    items: Sequence[Order]


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateOrder(ToDictMixin):
    id: UUID
    user_id: UUID | Unset = UNSET
    pickup_address_id: UUID | Unset = UNSET
    status: OrderStatus | Unset = UNSET
    products: Sequence[Mapping] | Unset = UNSET
    address: str | Unset = UNSET
    delivered_at: date | Unset = UNSET
    price: int | Unset = UNSET
