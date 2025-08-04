from typing import Any
from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from bakery.domains.entities.pickup_address import (
    CreatePickupAddress,
    UpdatePickupAddress,
)
from bakery.domains.services.pickup_address import PickupAddressService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminPickupAddress


async def on_view_pickup_address_clicked(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["pickup_address_id"] = item_id
    await manager.start(
        state=AdminPickupAddress.view_one,
        data=dict(pickup_address_id=item_id),
    )


async def on_add_clicked(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminPickupAddress.add_name)


async def on_name_input(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
) -> None:
    manager.dialog_data["name"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminPickupAddress.add_confirm)


async def on_create_pickup_address(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    container = manager.middleware_data["dishka_container"]
    service: PickupAddressService = await container.get(PickupAddressService)
    uow: AbstractUow = await container.get(AbstractUow)
    try:
        async with uow:
            pickup_address = await service.create(
                input_dto=CreatePickupAddress(
                    name=manager.dialog_data["name"] or manager.start_data["name"],  # type: ignore
                )
            )
        await manager.start(
            state=AdminPickupAddress.view_one,
            data=dict(pickup_address_id=str(pickup_address.id)),
        )
    except EntityAlreadyExistsException:
        await callback.answer(
            text="Такой адрес уже есть! Выберите другой.",
        )
        await manager.switch_to(AdminPickupAddress.update_name)


async def on_update_clicked(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    pickup_address_id = manager.start_data.get(  # type: ignore[union-attr]
        "pickup_address_id"
    ) or manager.dialog_data.get(  # type: ignore[union-attr]
        "pickup_address_id"
    )
    await manager.start(
        state=AdminPickupAddress.update_name,
        data=dict(pickup_address_id=pickup_address_id),
        mode=StartMode.RESET_STACK,
    )


async def on_update_name_input(
    message: Message, widget: MessageInput, manager: DialogManager
) -> None:
    manager.dialog_data["name"] = message.text.strip()  # type: ignore[union-attr]
    await manager.switch_to(AdminPickupAddress.update_confirm)


async def on_update_pickup_address(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    pickup_address_id = UUID(manager.start_data["pickup_address_id"])  # type: ignore
    service: PickupAddressService = await manager.middleware_data[
        "dishka_container"
    ].get(PickupAddressService)
    uow: AbstractUow = await manager.middleware_data["dishka_container"].get(
        AbstractUow
    )
    try:
        async with uow:
            await service.update_by_id(
                input_dto=UpdatePickupAddress(
                    id=pickup_address_id,
                    name=manager.dialog_data["name"],
                )
            )
        await manager.start(
            AdminPickupAddress.view_one,
            data=dict(pickup_address_id=str(pickup_address_id)),
            mode=StartMode.RESET_STACK,
        )
    except EntityAlreadyExistsException:
        await callback.answer(
            text="Такой адрес уже есть! Выберите другой.",
        )
        await manager.switch_to(AdminPickupAddress.update_name)


async def go_to_confirm_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminPickupAddress.confirm_delete)


async def on_confirm_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    container = manager.middleware_data["dishka_container"]
    service: PickupAddressService = await container.get(PickupAddressService)
    uow: AbstractUow = await container.get(AbstractUow)
    address_id = UUID(manager.dialog_data["pickup_address_id"])
    try:
        async with uow:
            await service.delete_by_id(input_id=address_id)
    except EntityNotFoundException:
        await callback.answer("Адрес не найден", show_alert=True)
        return
    await manager.switch_to(AdminPickupAddress.view_all)


async def on_cancel_delete(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    pickup_address_id = manager.dialog_data["pickup_address_id"]
    await manager.start(
        state=AdminPickupAddress.view_one,
        data=dict(pickup_address_id=pickup_address_id),
        mode=StartMode.RESET_STACK,
    )
