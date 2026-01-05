from typing import NoReturn

from sqlalchemy import insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.delivery_cost import convert_delivery_cost
from bakery.adapters.database.tables import DeliveryCostTable
from bakery.application.exceptions import (
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.delivery_cost import (
    CreateDeliveryCost,
    DeliveryCost,
    UpdateDeliveryCost,
)
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage


class DeliveryCostStorage(IDeliveryCostStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateDeliveryCost) -> DeliveryCost:
        stmt = (
            insert(DeliveryCostTable)
            .values(**input_dto.to_dict())
            .returning(DeliveryCostTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_delivery_cost(result=result)

    async def get_last(self) -> DeliveryCost | None:
        stmt = (
            select(DeliveryCostTable)
            .order_by(DeliveryCostTable.created_at.desc())
            .limit(1)
        )
        result = await self.__session.scalar(stmt)
        return convert_delivery_cost(result=result) if result else None

    async def update_by_id(self, *, input_dto: UpdateDeliveryCost) -> DeliveryCost:
        stmt = (
            update(DeliveryCostTable)
            .where(DeliveryCostTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(DeliveryCostTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(
                entity=DeliveryCost, entity_id=input_dto.id
            ) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_delivery_cost(result=result)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        raise StorageException(self.__class__.__name__) from e
