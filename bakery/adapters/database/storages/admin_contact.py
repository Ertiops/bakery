from typing import NoReturn

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.admin_contact import convert_admin_contact
from bakery.adapters.database.tables import AdminContactTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.admin_contact import (
    AdminContact,
    CreateAdminContact,
    UpdateAdminContact,
)
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage


class AdminContactStorage(IAdminContactStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateAdminContact) -> AdminContact:
        stmt = (
            insert(AdminContactTable)
            .values(**input_dto.to_dict())
            .returning(AdminContactTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_admin_contact(result=result)

    async def get_last(self) -> AdminContact | None:
        stmt = (
            select(AdminContactTable)
            .order_by(AdminContactTable.created_at.desc())
            .limit(1)
        )
        result = await self.__session.scalar(stmt)
        return convert_admin_contact(result=result) if result else None

    async def update_by_id(self, *, input_dto: UpdateAdminContact) -> AdminContact:
        stmt = (
            update(AdminContactTable)
            .where(AdminContactTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(AdminContactTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(
                entity=AdminContact, entity_id=input_dto.id
            ) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_admin_contact(result=result)

    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        stmt = delete(AdminContactTable)
        if input_dto.deleted_at is not None:
            stmt = stmt.where(AdminContactTable.deleted_at <= input_dto.deleted_at)
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "ix__admin_contacts__phone":
                raise EntityAlreadyExistsException(
                    "AdminContact with such phone already exists"
                )
        raise StorageException(self.__class__.__name__) from e
