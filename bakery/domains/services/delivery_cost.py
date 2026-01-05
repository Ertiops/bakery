from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.delivery_cost import (
    CreateDeliveryCost,
    DeliveryCost,
    UpdateDeliveryCost,
)
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage


class DeliveryCostService:
    __delivery_cost_storage: IDeliveryCostStorage

    def __init__(self, delivery_cost_storage: IDeliveryCostStorage) -> None:
        self.__delivery_cost_storage = delivery_cost_storage

    async def create(self, *, input_dto: CreateDeliveryCost) -> DeliveryCost:
        return await self.__delivery_cost_storage.create(input_dto=input_dto)

    async def get_last(self) -> DeliveryCost:
        delivery_cost = await self.__delivery_cost_storage.get_last()
        if delivery_cost is None:
            raise EntityNotFoundException(entity=DeliveryCost, entity_id=None)
        return delivery_cost

    async def update_by_id(self, *, input_dto: UpdateDeliveryCost) -> DeliveryCost:
        return await self.__delivery_cost_storage.update_by_id(input_dto=input_dto)
