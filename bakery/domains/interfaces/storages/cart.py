from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.cart import (
    Cart,
    CartListParams,
    CartWProduct,
    CreateCart,
    GetCartByUserProductIds,
)


class ICartStorage(Protocol):
    @abstractmethod
    async def create_or_update(self, *, input_dto: CreateCart) -> Cart:
        raise NotImplementedError

    @abstractmethod
    async def get_w_product_by_user_product_ids(
        self, *, input_dto: GetCartByUserProductIds
    ) -> CartWProduct | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *, input_dto: CartListParams) -> Sequence[CartWProduct]:
        raise NotImplementedError

    @abstractmethod
    async def delete_hard_by_user_id(self, *, input_id: UUID) -> None:
        raise NotImplementedError
