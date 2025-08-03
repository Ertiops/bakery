from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from bakery.domains.entities.cart import Cart, CartListParams, CartWProduct, CreateCart


class ICartStorage(Protocol):
    @abstractmethod
    async def create_or_update(self, *, input_dto: CreateCart) -> Cart:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *, input_dto: CartListParams) -> Sequence[CartWProduct]:
        raise NotImplementedError
