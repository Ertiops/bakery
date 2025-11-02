import logging
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bakery.application.exceptions import (
    EntityNotFoundException,
)
from bakery.domains.entities.admin_contact import CreateAdminContact, UpdateAdminContact
from bakery.domains.services.admin_contact import AdminContactService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminAdminContact

log = logging.getLogger(__name__)


async def open_admin_contact(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
) -> None:
    container = dialog_manager.middleware_data["dishka_container"]
    service: AdminContactService = await container.get(AdminContactService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        try:
            admin_contact = await service.get_last()
        except EntityNotFoundException:
            await dialog_manager.start(
                state=AdminAdminContact.add_choice,
                mode=StartMode.RESET_STACK,
            )
            return
    await dialog_manager.start(
        state=AdminAdminContact.view_one,
        mode=StartMode.RESET_STACK,
        data=dict(
            contact_id=str(admin_contact.id),
            name=admin_contact.name,
            tg_username=admin_contact.tg_username,
        ),
    )


async def on_create_name_input(
    message: Message,
    _: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data["name"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminAdminContact.add_tg_username)


async def on_create_tg_username_input(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    text = (message.text or "").strip()
    if not text.startswith("@"):
        return
    manager.dialog_data["tg_username"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminAdminContact.add_confirm)


async def on_update_name_input(
    message: Message,
    _: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data["name"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminAdminContact.update_tg_username)


async def on_update_tg_username_input(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    text = (message.text or "").strip()
    if not text.startswith("@"):
        return
    manager.dialog_data["tg_username"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminAdminContact.update_confirm)


async def on_create(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message is None:
        return
    container = manager.middleware_data["dishka_container"]
    service: AdminContactService = await container.get(AdminContactService)
    uow: AbstractUow = await container.get(AbstractUow)
    log.info("Creating Admin Contact")
    async with uow:
        admin_contact = await service.create(
            input_dto=CreateAdminContact(
                name=manager.dialog_data["name"],
                tg_username=manager.dialog_data["tg_username"],
            )
        )
    await manager.start(
        state=AdminAdminContact.view_one,
        mode=StartMode.RESET_STACK,
        data=dict(
            contact_id=str(admin_contact.id),
            name=admin_contact.name,
            tg_username=admin_contact.tg_username,
        ),
    )


async def on_cancel_creation(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message is None:
        return
    await manager.start(
        state=AdminAdminContact.add_choice,
        mode=StartMode.RESET_STACK,
    )


async def on_cancel_update(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message is None:
        return
    await manager.start(
        state=AdminAdminContact.view_one,
        mode=StartMode.RESET_STACK,
        data=manager.start_data,
    )


async def on_update(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    if callback.message is None:
        return
    container = manager.middleware_data["dishka_container"]
    service: AdminContactService = await container.get(AdminContactService)
    uow: AbstractUow = await container.get(AbstractUow)
    log.info("Creating Admin Contact")
    async with uow:
        admin_contact = await service.update_by_id(
            input_dto=UpdateAdminContact(
                id=UUID(manager.start_data["contact_id"]),  # type: ignore
                name=manager.dialog_data["name"],
                tg_username=manager.dialog_data["tg_username"],
            )
        )
    await manager.start(
        state=AdminAdminContact.view_one,
        mode=StartMode.RESET_STACK,
        data=dict(
            contact_id=str(admin_contact.id),
            name=admin_contact.name,
            tg_username=admin_contact.tg_username,
        ),
    )
