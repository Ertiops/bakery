from uuid import UUID

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserBlacklistListParams,
    UserClearExclusionParams,
    UserExclusionParams,
    UserList,
    UserListParams,
    UserPhoneSearchParams,
)
from bakery.domains.interfaces.storages.user import IUserStorage


class UserService:
    __user_storage: IUserStorage

    def __init__(self, user_storage: IUserStorage) -> None:
        self.__user_storage = user_storage

    async def create(self, *, input_dto: CreateUser) -> User:
        return await self.__user_storage.create(input_dto=input_dto)

    async def get_by_id(self, *, input_id: UUID) -> User:
        user = await self.__user_storage.get_by_id(input_id=input_id)
        if user is None:
            raise EntityNotFoundException(entity=User, entity_id=input_id)
        return user

    async def get_by_tg_id(self, *, input_id: int) -> User:
        user = await self.__user_storage.get_by_tg_id(input_id=input_id)
        if user is None:
            raise EntityNotFoundException(entity=User, entity_id=input_id)
        return user

    async def get_admin(self) -> User:
        user = await self.__user_storage.get_admin()
        if user is None:
            raise EntityNotFoundException(entity=User, entity_id=None)
        return user

    async def get_list(self, *, input_dto: UserListParams) -> UserList:
        total = await self.__user_storage.count(input_dto=input_dto)
        items = await self.__user_storage.get_list(input_dto=input_dto)
        return UserList(total=total, items=items)

    async def get_blacklist(
        self, *, input_dto: UserBlacklistListParams, user: User
    ) -> UserList:
        _ = user
        total = await self.__user_storage.count_blacklist(input_dto=input_dto)
        items = await self.__user_storage.get_blacklist_list(input_dto=input_dto)
        return UserList(total=total, items=items)

    async def search_by_phone(
        self, *, input_dto: UserPhoneSearchParams, user: User
    ) -> UserList:
        _ = user
        total = await self.__user_storage.count_by_phone(input_dto=input_dto)
        items = await self.__user_storage.get_list_by_phone(input_dto=input_dto)
        return UserList(total=total, items=items)

    async def update_by_id(self, *, input_dto: UpdateUser) -> User:
        if not await self.__user_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=User, entity_id=input_dto.id)
        return await self.__user_storage.update_by_id(input_dto=input_dto)

    async def set_exclusion_reason(
        self, *, input_dto: UserExclusionParams, user: User
    ) -> User:
        _ = user
        if not await self.__user_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=User, entity_id=input_dto.id)
        return await self.__user_storage.update_by_id(
            input_dto=UpdateUser(
                id=input_dto.id,
                exclusion_reason=input_dto.reason,
            )
        )

    async def clear_exclusion_reason(
        self, *, input_dto: UserClearExclusionParams, user: User
    ) -> User:
        _ = user
        if not await self.__user_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=User, entity_id=input_dto.id)
        return await self.__user_storage.update_by_id(
            input_dto=UpdateUser(
                id=input_dto.id,
                exclusion_reason=None,
            )
        )

    async def delete_by_id(self, *, input_id: UUID) -> None:
        if not await self.__user_storage.exists_by_id(input_id=input_id):
            raise EntityNotFoundException(entity=User, entity_id=input_id)
        await self.__user_storage.delete_by_id(input_id=input_id)

    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        await self.__user_storage.hard_delete_list(input_dto=input_dto)
