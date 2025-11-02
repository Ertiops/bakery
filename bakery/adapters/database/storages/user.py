from collections.abc import Sequence
from datetime import UTC, datetime
from typing import NoReturn
from uuid import UUID

from sqlalchemy import exists, func, insert, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.converters.user import convert_user
from bakery.adapters.database.tables import UserTable
from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
    StorageException,
)
from bakery.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserListParams,
    UserRole,
)
from bakery.domains.interfaces.storages.user import IUserStorage


class UserStorage(IUserStorage):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def create(self, *, input_dto: CreateUser) -> User:
        stmt = insert(UserTable).values(**input_dto.to_dict()).returning(UserTable)
        try:
            result = (await self.__session.scalars(stmt)).one()
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_user(result=result)

    async def get_by_id(self, *, input_id: UUID) -> User | None:
        stmt = select(UserTable).where(
            UserTable.id == input_id, UserTable.deleted_at.is_(None)
        )
        result = await self.__session.scalar(stmt)
        return convert_user(result=result) if result else None

    async def get_by_tg_id(self, *, input_id: int) -> User | None:
        stmt = select(UserTable).where(
            UserTable.tg_id == input_id, UserTable.deleted_at.is_(None)
        )
        result = await self.__session.scalar(stmt)
        return convert_user(result=result) if result else None

    async def get_admin(self) -> User | None:
        stmt = (
            select(UserTable)
            .where(
                UserTable.role == UserRole.ADMIN,
                UserTable.deleted_at.is_(None),
            )
            .limit(1)
        )
        result = await self.__session.scalar(stmt)
        return convert_user(result=result) if result else None

    async def get_list(self, *, input_dto: UserListParams) -> Sequence[User]:
        stmt = (
            select(UserTable)
            .where(UserTable.deleted_at.is_(None))
            .limit(input_dto.limit)
            .offset(input_dto.offset)
        )
        result = await self.__session.scalars(stmt)
        return [convert_user(result=r) for r in result]

    async def count(self, *, input_dto: UserListParams) -> int:
        stmt = (
            select(func.count())
            .select_from(UserTable)
            .where(UserTable.deleted_at.is_(None))
        )
        return await self.__session.scalar(stmt) or 0

    async def exists_by_id(self, *, input_id: UUID) -> bool:
        stmt = select(
            exists().where(UserTable.id == input_id, UserTable.deleted_at.is_(None))
        )
        return bool(await self.__session.scalar(stmt))

    async def update_by_id(self, *, input_dto: UpdateUser) -> User:
        stmt = (
            update(UserTable)
            .where(UserTable.id == input_dto.id)
            .values(**input_dto.to_dict())
            .returning(UserTable)
        )
        try:
            result = (await self.__session.scalars(stmt)).one()
        except NoResultFound as e:
            raise EntityNotFoundException(entity=User, entity_id=input_dto.id) from e
        except IntegrityError as e:
            self.__raise_exception(e)
        return convert_user(result=result)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        stmt = (
            update(UserTable)
            .where(UserTable.id == input_id)
            .values(deleted_at=datetime.now(tz=UTC))
        )
        await self.__session.execute(stmt)

    def __raise_exception(self, e: DBAPIError) -> NoReturn:
        constraint = e.__cause__.__cause__.constraint_name  # type: ignore[union-attr]
        match constraint:
            case "ix__users__phone":
                raise EntityAlreadyExistsException(
                    "User with such phone already exists"
                )
            case "ix__users__tg_id":
                raise EntityAlreadyExistsException(
                    "User with such tg_id already exists"
                )
        raise StorageException(self.__class__.__name__) from e
