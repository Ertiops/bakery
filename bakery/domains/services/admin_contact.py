from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.admin_contact import (
    AdminContact,
    CreateAdminContact,
    UpdateAdminContact,
)
from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage


class AdminContactService:
    __admin_contact_storage: IAdminContactStorage

    def __init__(self, admin_contact_storage: IAdminContactStorage) -> None:
        self.__admin_contact_storage = admin_contact_storage

    async def create(self, *, input_dto: CreateAdminContact) -> AdminContact:
        return await self.__admin_contact_storage.create(input_dto=input_dto)

    async def get_last(self) -> AdminContact:
        admin_contact = await self.__admin_contact_storage.get_last()
        if admin_contact is None:
            raise EntityNotFoundException(entity=AdminContact, entity_id=None)
        return admin_contact

    async def update_by_id(self, *, input_dto: UpdateAdminContact) -> AdminContact:
        return await self.__admin_contact_storage.update_by_id(input_dto=input_dto)
