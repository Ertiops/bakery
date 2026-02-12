from collections.abc import Sequence
from typing import NoReturn
from uuid import UUID

from sqlalchemy import delete, exists, func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.base import now_with_tz
from bakery.adapters.database.converters.pickup_address import (
    convert_pickup_address,
)
from bakery.adapters.database.tables import PickupAddressTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.pickup_address import (
    CreatePickupAddress,
    PickupAddress,
    PickupAddressListParams,
    UpdatePickupAddress,
)
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage


class PickupAddressStorage(IPickupAddressStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreatePickupAddress) -> PickupAddress:
        stmt = (
            insert(PickupAddressTable)
            .values(**input_dto.to_dict())
            .returning(PickupAddressTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_pickup_address(result=result)

    async def get_by_id(self, *, input_id: UUID) -> PickupAddress | None:
        stmt = select(PickupAddressTable).where(
            PickupAddressTable.id == input_id, PickupAddressTable.deleted_at.is_(None)
        )
        result = await self.__session.scalar(stmt)
        return convert_pickup_address(result=result) if result else None

    async def get_list(
        self, *, input_dto: PickupAddressListParams
    ) -> Sequence[PickupAddress]:
        stmt = (
            select(PickupAddressTable)
            .where(PickupAddressTable.deleted_at.is_(None))
            .order_by(PickupAddressTable.created_at)
            .limit(input_dto.limit)
            .offset(input_dto.offset)
        )
        result = await self.__session.scalars(stmt)
        return [convert_pickup_address(result=r) for r in result]

    async def count(self, *, input_dto: PickupAddressListParams) -> int:
        stmt = (
            select(func.count())
            .select_from(PickupAddressTable)
            .where(PickupAddressTable.deleted_at.is_(None))
        )
        return await self.__session.scalar(stmt) or 0

    async def exists_by_id(self, *, input_id: UUID) -> bool:
        stmt = select(
            exists().where(
                PickupAddressTable.id == input_id,
                PickupAddressTable.deleted_at.is_(None),
            )
        )
        return bool(await self.__session.scalar(stmt))

    async def update_by_id(self, *, input_dto: UpdatePickupAddress) -> PickupAddress:
        stmt = (
            update(PickupAddressTable)
            .where(PickupAddressTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(PickupAddressTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(
                entity=PickupAddress, entity_id=input_dto.id
            ) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_pickup_address(result=result)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        stmt = (
            update(PickupAddressTable)
            .where(PickupAddressTable.id == input_id)
            .values(deleted_at=now_with_tz())
        )
        await self.__session.execute(stmt)

    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        stmt = delete(PickupAddressTable)
        if input_dto.deleted_at is not None:
            stmt = stmt.where(PickupAddressTable.deleted_at <= input_dto.deleted_at)
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "ix__pickup_addresses__name":
                raise EntityAlreadyExistsException(
                    "PickupAddress with such name already exists"
                )
        raise StorageException(self.__class__.__name__) from e
