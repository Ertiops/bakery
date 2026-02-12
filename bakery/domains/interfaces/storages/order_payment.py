from abc import abstractmethod
from typing import Protocol

from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.entities.order_payment import (
    CreateOrderPayment,
    OrderPayment,
    UpdateOrderPayment,
)


class IOrderPaymentStorage(Protocol):
    @abstractmethod
    async def create(self, *, input_dto: CreateOrderPayment) -> OrderPayment:
        raise NotImplementedError

    @abstractmethod
    async def get_last(self) -> OrderPayment | None:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, *, input_dto: UpdateOrderPayment) -> OrderPayment:
        raise NotImplementedError

    @abstractmethod
    async def hard_delete_list(self, *, input_dto: HardDeleteListParams) -> None:
        raise NotImplementedError
