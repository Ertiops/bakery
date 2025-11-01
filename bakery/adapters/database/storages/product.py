from collections.abc import Sequence
from datetime import UTC, datetime
from typing import NoReturn
from uuid import UUID

from sqlalchemy import exists, func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.product import convert_product
from bakery.adapters.database.tables import ProductTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.product import (
    CreateProduct,
    Product,
    ProductListParams,
    UpdateProduct,
)
from bakery.domains.interfaces.storages.product import IProductStorage


class ProductStorage(IProductStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateProduct) -> Product:
        stmt = (
            insert(ProductTable).values(**input_dto.to_dict()).returning(ProductTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_product(result=result)

    async def get_by_id(self, *, input_id: UUID) -> Product | None:
        stmt = select(ProductTable).where(
            ProductTable.id == input_id, ProductTable.deleted_at.is_(None)
        )
        result = await self.__session.scalar(stmt)
        return convert_product(result=result) if result else None

    async def get_list(self, *, input_dto: ProductListParams) -> Sequence[Product]:
        stmt = (
            select(ProductTable)
            .where(ProductTable.deleted_at.is_(None))
            .order_by(ProductTable.name)
            .limit(input_dto.limit)
            .offset(input_dto.offset)
        )
        if input_dto.category:
            stmt = stmt.where(ProductTable.category == input_dto.category)
        result = await self.__session.scalars(stmt)
        return [convert_product(result=r) for r in result]

    async def count(self, *, input_dto: ProductListParams) -> int:
        stmt = (
            select(func.count())
            .select_from(ProductTable)
            .where(ProductTable.deleted_at.is_(None))
        )
        if input_dto.category:
            stmt = stmt.where(ProductTable.category == input_dto.category)
        return await self.__session.scalar(stmt) or 0

    async def exists_by_id(self, *, input_id: UUID) -> bool:
        stmt = select(
            exists().where(
                ProductTable.id == input_id, ProductTable.deleted_at.is_(None)
            )
        )
        return bool(await self.__session.scalar(stmt))

    async def update_by_id(self, *, input_dto: UpdateProduct) -> Product:
        stmt = (
            update(ProductTable)
            .where(ProductTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(ProductTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(entity=Product, entity_id=input_dto.id) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_product(result=result)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        stmt = (
            update(ProductTable)
            .where(ProductTable.id == input_id)
            .values(deleted_at=datetime.now(tz=UTC))
        )
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "ix__products__name":
                raise EntityAlreadyExistsException(
                    "Product with such title already exists"
                )
        raise StorageException(self.__class__.__name__) from e
