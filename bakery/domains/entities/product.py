from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, unique
from uuid import UUID

from bakery.domains.entities.common import Pagination, ToDictMixin


@unique
class ProductCategory(StrEnum):
    BREAD = "bread"
    OIL = "oil"
    FLOUR = "flour"
    DESSERT = "dessert"
    NOODLE = "noodle"
    OTHER = "other"


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateProduct(ToDictMixin):
    name: str
    description: str
    category: ProductCategory
    weight: int
    volume: int
    protein: int
    fat: int
    carbohydrate: int
    price: int


@dataclass(frozen=True, kw_only=True, slots=True)
class Product:
    id: UUID
    name: str
    description: str
    category: ProductCategory
    weight: int
    volume: int
    protein: int
    fat: int
    carbohydrate: int
    price: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class UpdateProduct(ToDictMixin):
    id: UUID
    name: str
    description: str
    category: ProductCategory
    weight: int
    volume: int
    protein: int
    fat: int
    carbohydrate: int
    price: int


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductListParams(Pagination):
    category: ProductCategory | None


@dataclass(frozen=True, kw_only=True, slots=True)
class ProductList:
    total: int
    items: Sequence[Product]
