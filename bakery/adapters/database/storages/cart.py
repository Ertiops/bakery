from collections.abc import Sequence
from typing import NoReturn

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.base import now_with_tz
from bakery.adapters.database.converters.cart import (
    convert_cart_to_dto,
    convert_cart_w_product_to_dto,
)
from bakery.adapters.database.tables import CartTable, ProductTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    ForeignKeyViolationException,
    StorageException,
)
from bakery.domains.entities.cart import Cart, CartListParams, CartWProduct, CreateCart
from bakery.domains.interfaces.storages.cart import ICartStorage


class CartStorage(ICartStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create_or_update(self, *, input_dto: CreateCart) -> Cart:
        stmt = (
            insert(CartTable)
            .values(**input_dto.to_dict())
            .on_conflict_do_update(
                index_elements=[CartTable.user_id, CartTable.product_id],
                set_=dict(
                    quantity=input_dto.quantity,
                    updated_at=now_with_tz(),
                ),
                index_where=CartTable.deleted_at.is_(None),
            )
            .returning(CartTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_cart_to_dto(result=result)

    async def get_list(self, *, input_dto: CartListParams) -> Sequence[CartWProduct]:
        stmt = (
            select(CartTable, ProductTable)
            .join(ProductTable, CartTable.product_id == ProductTable.id)
            .where(
                CartTable.deleted_at.is_(None),
                ProductTable.deleted_at.is_(None),
            )
        )
        if input_dto.user_id:
            stmt = stmt.where(CartTable.user_id == input_dto.user_id)
        if input_dto.has_non_zero_quantity:
            stmt = stmt.where(CartTable.quantity > 0)
        result = (await self.__session.execute(stmt)).all()
        return [convert_cart_w_product_to_dto(result=r._tuple()) for r in result]

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "fk__carts__user_id__users":
                raise ForeignKeyViolationException("User with such id doesn't exist")
            case "fk__carts__product_id__products":
                raise ForeignKeyViolationException("Product with such id doesn't exist")
            case "ix__carts__user_id_product_id":
                raise EntityAlreadyExistsException(
                    "Cart with such user_id already exists"
                )
        raise StorageException(self.__class__.__name__) from e
