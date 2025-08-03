from collections.abc import Sequence

from bakery.domains.entities.cart import Cart, CartListParams, CartWProduct, CreateCart
from bakery.domains.interfaces.storages.cart import ICartStorage


class CartService:
    __cart_storage: ICartStorage

    def __init__(
        self,
        cart_storage: ICartStorage,
    ) -> None:
        self.__cart_storage = cart_storage

    async def create_or_update(self, *, input_dto: CreateCart) -> Cart:
        return await self.__cart_storage.create_or_update(input_dto=input_dto)

    async def get_list(self, *, input_dto: CartListParams) -> Sequence[CartWProduct]:
        return await self.__cart_storage.get_list(input_dto=input_dto)
