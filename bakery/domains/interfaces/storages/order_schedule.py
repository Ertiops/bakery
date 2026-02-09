from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.order_schedule import (
    CreateOrderSchedule,
    OrderSchedule,
    UpdateOrderSchedule,
)


class IOrderScheduleStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateOrderSchedule) -> OrderSchedule:
        raise NotImplementedError

    @abstractmethod
    async def get_last(self) -> OrderSchedule | None:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateOrderSchedule) -> OrderSchedule:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, *, input_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        raise NotImplementedError
