from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from bakery.domains.entities.common import ToDictMixin
from bakery.domains.entities.product import Product


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateCart(ToDictMixin):
    user_id: UUID
    product_id: UUID
    quantity: int


@dataclass(frozen=True, kw_only=True, slots=True)
class Cart(ToDictMixin):
    user_id: UUID
    product_id: UUID
    quantity: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class CartWProduct(ToDictMixin):
    user_id: UUID
    quantity: int
    product: Product
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class CartListParams:
    user_id: UUID | None
    has_non_zero_quantity: bool


@dataclass(frozen=True, kw_only=True, slots=True)
class GetCartByUserProductIds:
    user_id: UUID
    product_id: UUID
