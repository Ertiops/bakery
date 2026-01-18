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
    CANCELLED = "cancelled"
    PAID = "paid"


@unique
class UserOrderStatus(StrEnum):
    CREATED = "created"
    DELIVERED = "delivered"
    PAID = "paid"


USER_ORDER_STATUS_MAP: Mapping[UserOrderStatus, Sequence[OrderStatus]] = {
    UserOrderStatus.CREATED: (
        OrderStatus.CREATED,
        OrderStatus.CHANGED,
    ),
    UserOrderStatus.DELIVERED: (OrderStatus.DELIVERED,),
    UserOrderStatus.PAID: (OrderStatus.PAID,),
}


class OrderProduct(TypedDict):
    name: str
    price: int
    quantity: int


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrderAsUser:
    user_id: UUID
    pickup_address_name: str
    products: Sequence[OrderProduct]
    delivered_at: date
    total_price: int
    delivery_price: int


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateOrder(ToDictMixin):
    user_id: UUID
    pickup_address_name: str
    status: OrderStatus
    products: Sequence[OrderProduct]
    delivered_at: date
    total_price: int
    delivery_price: int
    delivered_at_id: int
    payment_file_id: str


@dataclass(frozen=True, kw_only=True, slots=True)
class Order:
    id: UUID
    user_id: UUID
    pickup_address_name: str
    status: OrderStatus
    products: Sequence[OrderProduct]
    delivered_at: date
    total_price: int
    delivery_price: int
    delivered_at_id: int
    payment_file_id: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class OrderListParams(Pagination):
    user_id: UUID | None = None
    pickup_address_name: str | None = None
    statuses: Sequence[OrderStatus] | None = None
    delivered_at: date | None = None
    created_at_period: tuple[datetime, datetime] | None = None


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
    total_price: int | Unset = UNSET
    delivery_price: int | Unset = UNSET
    payment_file_id: str | Unset = UNSET
