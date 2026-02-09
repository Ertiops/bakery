from abc import abstractmethod
from typing import Protocol

from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.delivery_cost import (
    CreateDeliveryCost,
    DeliveryCost,
    UpdateDeliveryCost,
)


class IDeliveryCostStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateDeliveryCost) -> DeliveryCost:
        raise NotImplementedError

    @abstractmethod
    async def get_last(self) -> DeliveryCost | None:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateDeliveryCost) -> DeliveryCost:
        raise NotImplementedError

    @abstractmethod
    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        raise NotImplementedError
