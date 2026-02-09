from abc import abstractmethod
from typing import Protocol

from bakery.domains.entities.admin_contact import (
    AdminContact,
    CreateAdminContact,
    UpdateAdminContact,
)
from bakery.domains.entities.common import HardDeleteListParams


class IAdminContactStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateAdminContact) -> AdminContact:
        raise NotImplementedError

    @abstractmethod
    async def get_last(self) -> AdminContact | None:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateAdminContact) -> AdminContact:
        raise NotImplementedError

    @abstractmethod
    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        raise NotImplementedError
