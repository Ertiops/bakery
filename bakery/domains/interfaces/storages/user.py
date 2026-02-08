from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.user import (
    CreateUser,
    UpdateUser,
    User,
    UserBlacklistListParams,
    UserFakeListParams,
    UserFakeSearchParams,
    UserListParams,
    UserPhoneSearchParams,
)


class IUserStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateUser) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, input_id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_tg_id(self, *, input_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_admin(self) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *, input_dto: UserListParams) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_blacklist_list(
        self, *, input_dto: UserBlacklistListParams
    ) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_fake_list(self, *, input_dto: UserFakeListParams) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_fake_list_by_phone(
        self, *, input_dto: UserFakeSearchParams
    ) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def count(self, *, input_dto: UserListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_blacklist(self, *, input_dto: UserBlacklistListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_fake(self, *, input_dto: UserFakeListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_fake_by_phone(self, *, input_dto: UserFakeSearchParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_list_by_phone(
        self, *, input_dto: UserPhoneSearchParams
    ) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def count_by_phone(self, *, input_dto: UserPhoneSearchParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self, *, input_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateUser) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, input_id: UUID) -> None:
        raise NotImplementedError
