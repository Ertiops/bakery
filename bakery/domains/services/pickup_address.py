from uuid import UUID

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.pickup_address import (
    CreatePickupAddress,
    PickupAddress,
    PickupAddressList,
    PickupAddressListParams,
    UpdatePickupAddress,
)
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage


class PickupAddressService:
    __pickup_address_storage: IPickupAddressStorage

    def __init__(self, pickup_address_storage: IPickupAddressStorage) -> None:
        self.__pickup_address_storage = pickup_address_storage

    async def create(self, *, input_dto: CreatePickupAddress) -> PickupAddress:
        return await self.__pickup_address_storage.create(input_dto=input_dto)

    async def get_by_id(self, *, input_id: UUID) -> PickupAddress:
        address = await self.__pickup_address_storage.get_by_id(input_id=input_id)
        if address is None:
            raise EntityNotFoundException(entity=PickupAddress, entity_id=input_id)
        return address

    async def get_list(
        self, *, input_dto: PickupAddressListParams
    ) -> PickupAddressList:
        total = await self.__pickup_address_storage.count(input_dto=input_dto)
        items = await self.__pickup_address_storage.get_list(input_dto=input_dto)
        return PickupAddressList(total=total, items=items)

    async def update_by_id(self, *, input_dto: UpdatePickupAddress) -> PickupAddress:
        if not await self.__pickup_address_storage.exists_by_id(input_id=input_dto.id):
            raise EntityNotFoundException(entity=PickupAddress, entity_id=input_dto.id)
        return await self.__pickup_address_storage.update_by_id(input_dto=input_dto)

    async def delete_by_id(self, *, input_id: UUID) -> None:
        if not await self.__pickup_address_storage.exists_by_id(input_id=input_id):
            raise EntityNotFoundException(entity=PickupAddress, entity_id=input_id)
        await self.__pickup_address_storage.delete_by_id(input_id=input_id)
