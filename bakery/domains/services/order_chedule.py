from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.order_schedule import (
    CreateOrderSchedule,
    OrderSchedule,
    UpdateOrderSchedule,
)
from bakery.domains.interfaces.storages.order_schedule import IOrderScheduleStorage


class OrderScheduleService:
    __order_schedule_storage: IOrderScheduleStorage

    def __init__(self, order_schedule_storage: IOrderScheduleStorage) -> None:
        self.__order_schedule_storage = order_schedule_storage

    async def create(self, *, input_dto: CreateOrderSchedule) -> OrderSchedule:
        order_schedule = await self.__order_schedule_storage.get_last()
        if order_schedule is not None:
            await self.__order_schedule_storage.delete_by_id(input_id=order_schedule.id)
        return await self.__order_schedule_storage.create(input_dto=input_dto)

    async def get_last(self) -> OrderSchedule:
        order_schedule = await self.__order_schedule_storage.get_last()
        if order_schedule is None:
            raise EntityNotFoundException(entity=OrderSchedule, entity_id=None)
        return order_schedule

    async def update_by_id(self, *, input_dto: UpdateOrderSchedule) -> OrderSchedule:
        return await self.__order_schedule_storage.update_by_id(input_dto=input_dto)
