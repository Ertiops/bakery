from abc import abstractmethod
from collections.abc import Sequence
from datetime import date
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.order import (
    CreateOrder,
    Order,
    OrderListParams,
    OrderTopProductsParams,
    UpdateOrder,
)
from bakery.domains.entities.product import Product


class IOrderStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateOrder) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, input_id: UUID) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *, input_dto: OrderListParams) -> Sequence[Order]:
        raise NotImplementedError

    @abstractmethod
    async def count(self, *, input_dto: OrderListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_by_delivered_at(self, *, input_dto: date) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self, *, input_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateOrder) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, input_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_top_products_for_user(
        self,
        *,
        input_dto: OrderTopProductsParams,
    ) -> Sequence[Product]:
        raise NotImplementedError
