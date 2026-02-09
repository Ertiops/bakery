from uuid import UUID

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.product import (
    CreateProduct,
    Product,
    ProductList,
    ProductListParams,
    UpdateProduct,
)
from bakery.domains.interfaces.storages.product import IProductStorage


class ProductService:
    __product_storage: IProductStorage

    def __init__(self, product_storage: IProductStorage) -> None:
        self.__product_storage = product_storage

    async def create(self, *, input_dto: CreateProduct) -> Product:
        return await self.__product_storage.create(input_dto=input_dto)

    async def get_by_id(self, *, input_id: UUID) -> Product:
        product = await self.__product_storage.get_by_id(input_id=input_id)
        if product is None:
            raise EntityNotFoundException(entity=Product, entity_id=input_id)
        return product

    async def get_list(self, *, input_dto: ProductListParams) -> ProductList:
        total = await self.__product_storage.count(input_dto=input_dto)
        items = await self.__product_storage.get_list(input_dto=input_dto)
        return ProductList(total=total, items=items)

    async def update_by_id(self, *, input_dto: UpdateProduct) -> Product:
        if not await self.__product_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=Product, entity_id=input_dto.id)
        return await self.__product_storage.update_by_id(input_dto=input_dto)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        if not await self.__product_storage.exists_by_id(input_id=input_id):
            raise EntityNotFoundException(entity=Product, entity_id=input_id)
        await self.__product_storage.delete_by_id(input_id=input_id)

    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        await self.__product_storage.hard_delete_list(input_dto=input_dto)
