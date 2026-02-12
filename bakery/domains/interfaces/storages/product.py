from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.product import (
    CreateProduct,
    Product,
    ProductListParams,
    UpdateProduct,
)


class IProductStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateProduct) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, input_id: UUID) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *, input_dto: ProductListParams) -> Sequence[Product]:
        raise NotImplementedError

    @abstractmethod
    async def count(self, *, input_dto: ProductListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self, *, input_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateProduct) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, input_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        raise NotImplementedError
