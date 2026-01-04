from uuid import UUID

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order import (
    CreateOrder,
    Order,
    OrderList,
    OrderListParams,
    UpdateOrder,
)
from bakery.domains.entities.order_schedule import OrderSchedule
from bakery.domains.interfaces.storages.order import IOrderStorage
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage


class OrderService:
    __order_storage: IOrderStorage
    __order_schedule_storage: IOrderScheduleStorage

    def __init__(
        self,
        order_storage: IOrderStorage,
        order_schedule_storage: IOrderScheduleStorage,
    ) -> None:
        self.__order_storage = order_storage
        self.__order_schedule_storage = order_schedule_storage

    async def create(self, *, input_dto: CreateOrder) -> Order:
        # TODO: реальная логика создания заказа
        order_schedule = await self.__order_schedule_storage.get_last()
        if order_schedule is None:
            raise EntityNotFoundException(
                entity=OrderSchedule,
                entity_id=None,
            )
        return await self.__order_storage.create(input_dto=input_dto)

    async def get_by_id(self, *, input_id: UUID) -> Order:
        order = await self.__order_storage.get_by_id(input_id=input_id)
        if order is None:
            raise EntityNotFoundException(entity=Order, entity_id=input_id)
        return order

    async def get_list(self, *, input_dto: OrderListParams) -> OrderList:
        total = await self.__order_storage.count(input_dto=input_dto)
        items = await self.__order_storage.get_list(input_dto=input_dto)
        return OrderList(total=total, items=items)

    async def update_by_id(self, *, input_dto: UpdateOrder) -> Order:
        if not await self.__order_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=Order, entity_id=input_dto.id)
        return await self.__order_storage.update_by_id(input_dto=input_dto)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        if not await self.__order_storage.exists_by_id(input_id=input_id):
            raise EntityNotFoundException(entity=Order, entity_id=input_id)
        await self.__order_storage.delete_by_id(input_id=input_id)
