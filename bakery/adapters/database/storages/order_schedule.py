from datetime import UTC, datetime
from typing import NoReturn
from uuid import UUID

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.order_schedule import (
    convert_order_schedule_to_dto,
)
from bakery.adapters.database.tables import OrderScheduleTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.order_schedule import (
    CreateOrderSchedule,
    OrderSchedule,
    UpdateOrderSchedule,
)
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage


class OrderScheduleStorage(IOrderScheduleStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateOrderSchedule) -> OrderSchedule:
        stmt = (
            insert(OrderScheduleTable)
            .values(**input_dto.to_dict())
            .returning(OrderScheduleTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_order_schedule_to_dto(result=result)

    async def get_last(self) -> OrderSchedule | None:
        stmt = (
            select(OrderScheduleTable)
            .where(OrderScheduleTable.deleted_at.is_(None))
            .order_by(OrderScheduleTable.created_at.desc())
            .limit(1)
        )
        result = await self.__session.scalar(stmt)
        return convert_order_schedule_to_dto(result=result) if result else None

    async def update_by_id(self, *, input_dto: UpdateOrderSchedule) -> OrderSchedule:
        stmt = (
            update(OrderScheduleTable)
            .where(OrderScheduleTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(OrderScheduleTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(
                entity=OrderSchedule, entity_id=input_dto.id
            ) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_order_schedule_to_dto(result=result)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        stmt = (
            update(OrderScheduleTable)
            .where(OrderScheduleTable.id == input_id)
            .values(deleted_at=datetime.now(tz=UTC))
        )
        await self.__session.execute(stmt)

    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        stmt = delete(OrderScheduleTable)
        if input_dto.deleted_at is not None:
            stmt = stmt.where(OrderScheduleTable.deleted_at <= input_dto.deleted_at)
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        raise StorageException(self.__class__.__name__) from e
