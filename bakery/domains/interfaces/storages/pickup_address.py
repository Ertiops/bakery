from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.pickup_address import (
    CreatePickupAddress,
    PickupAddress,
    PickupAddressListParams,
    UpdatePickupAddress,
)


class IPickupAddressStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreatePickupAddress) -> PickupAddress:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, input_id: UUID) -> PickupAddress | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(
        self, *, input_dto: PickupAddressListParams
    ) -> Sequence[PickupAddress]:
        raise NotImplementedError

    @abstractmethod
    async def count(self, *, input_dto: PickupAddressListParams) -> int:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_id(self, *, input_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdatePickupAddress) -> PickupAddress:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, input_id: UUID) -> None:
        raise NotImplementedError
