from collections.abc import Sequence
from datetime import UTC, date, datetime
from typing import NoReturn
from uuid import UUID

from sqlalchemy import exists, func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.order import convert_order_to_dto
from bakery.adapters.database.tables import OrderTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    ForeignKeyViolationException,
    StorageException,
)
from bakery.domains.entities.order import (
    CreateOrder,
    Order,
    OrderListParams,
    UpdateOrder,
)
from bakery.domains.interfaces.storages.order import IOrderStorage


class OrderStorage(IOrderStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateOrder) -> Order:
        stmt = insert(OrderTable).values(**input_dto.to_dict()).returning(OrderTable)
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_order_to_dto(result=result)

    async def get_by_id(self, *, input_id: UUID) -> Order | None:
        stmt = select(OrderTable).where(
            OrderTable.id == input_id, OrderTable.deleted_at.is_(None)
        )
        result = await self.__session.scalar(stmt)
        return convert_order_to_dto(result=result) if result else None

    async def get_list(self, *, input_dto: OrderListParams) -> Sequence[Order]:
        stmt = (
            select(OrderTable)
            .where(OrderTable.deleted_at.is_(None))
            .order_by(OrderTable.created_at.desc())
            .limit(input_dto.limit)
            .offset(input_dto.offset)
        )
        if input_dto.user_id is not None:
            stmt = stmt.where(OrderTable.user_id == input_dto.user_id)
        if input_dto.pickup_address_name is not None:
            stmt = stmt.where(
                OrderTable.pickup_address_name == input_dto.pickup_address_name
            )
        if input_dto.statuses is not None:
            stmt = stmt.where(OrderTable.status.in_(input_dto.statuses))
        if input_dto.delivered_at is not None:
            stmt = stmt.where(OrderTable.delivered_at == input_dto.delivered_at)
        if input_dto.created_at_period is not None:
            stmt = stmt.where(
                OrderTable.created_at >= input_dto.created_at_period[0],
                OrderTable.created_at < input_dto.created_at_period[1],
            )

        result = await self.__session.scalars(stmt)
        return [convert_order_to_dto(result=r) for r in result]

    async def count(self, *, input_dto: OrderListParams) -> int:
        stmt = (
            select(func.count())
            .select_from(OrderTable)
            .where(OrderTable.deleted_at.is_(None))
        )
        if input_dto.user_id is not None:
            stmt = stmt.where(OrderTable.user_id == input_dto.user_id)
        if input_dto.pickup_address_name is not None:
            stmt = stmt.where(
                OrderTable.pickup_address_name == input_dto.pickup_address_name
            )
        if input_dto.statuses is not None:
            stmt = stmt.where(OrderTable.status.in_(input_dto.statuses))
        if input_dto.delivered_at is not None:
            stmt = stmt.where(OrderTable.delivered_at == input_dto.delivered_at)
        if input_dto.created_at_period is not None:
            stmt = stmt.where(
                OrderTable.created_at >= input_dto.created_at_period[0],
                OrderTable.created_at < input_dto.created_at_period[1],
            )

        return await self.__session.scalar(stmt) or 0

    async def count_by_delivered_at(self, *, input_dto: date) -> int:
        stmt = (
            select(func.count())
            .select_from(OrderTable)
            .where(
                OrderTable.delivered_at == input_dto,
            )
        )
        return await self.__session.scalar(stmt) or 0

    async def exists_by_id(self, *, input_id: UUID) -> bool:
        stmt = select(
            exists().where(OrderTable.id == input_id, OrderTable.deleted_at.is_(None))
        )
        return bool(await self.__session.scalar(stmt))

    async def update_by_id(self, *, input_dto: UpdateOrder) -> Order:
        stmt = (
            update(OrderTable)
            .where(OrderTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(OrderTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(entity=Order, entity_id=input_dto.id) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_order_to_dto(result=result)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        stmt = (
            update(OrderTable)
            .where(OrderTable.id == input_id)
            .values(deleted_at=datetime.now(tz=UTC))
        )
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "fk__orders__user_id__users":
                raise ForeignKeyViolationException("User with such id does not exist")
            case "fk__orders__pickup_address_id__pickup_addresses":
                raise ForeignKeyViolationException(
                    "Pickup address with such id does not exist"
                )
        raise StorageException(self.__class__.__name__) from e
