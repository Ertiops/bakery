from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.delivery_cost import CreateDeliveryCost, UpdateDeliveryCost
from bakery.domains.services.delivery_cost import DeliveryCostService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminDeliveryPrice


async def to_create_delivery_cost(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(AdminDeliveryPrice.create)


async def to_update_delivery_cost(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(AdminDeliveryPrice.update)


async def on_delivery_cost_entered_create(
    message: Message,
    widget: ManagedTextInput[int],
    manager: DialogManager,
    value: int,
) -> None:
    manager.dialog_data["delivery_cost_price"] = value
    await manager.switch_to(AdminDeliveryPrice.create_free_amount)


async def on_delivery_cost_entered_update(
    message: Message,
    widget: ManagedTextInput[int],
    manager: DialogManager,
    value: int,
) -> None:
    cost_id = manager.dialog_data.get("delivery_cost_id")
    if not cost_id:
        await manager.switch_to(AdminDeliveryPrice.view)
        return
    manager.dialog_data["delivery_cost_price"] = value
    await manager.switch_to(AdminDeliveryPrice.update_free_amount)


async def on_free_delivery_amount_entered_create(
    message: Message,
    widget: ManagedTextInput[int],
    manager: DialogManager,
    value: int,
) -> None:
    manager.dialog_data["delivery_cost_free_amount"] = value
    await manager.switch_to(AdminDeliveryPrice.create_confirm)


async def on_free_delivery_amount_entered_update(
    message: Message,
    widget: ManagedTextInput[int],
    manager: DialogManager,
    value: int,
) -> None:
    cost_id = manager.dialog_data.get("delivery_cost_id")
    if not cost_id:
        await manager.switch_to(AdminDeliveryPrice.view)
        return
    manager.dialog_data["delivery_cost_free_amount"] = value
    await manager.switch_to(AdminDeliveryPrice.update_confirm)


async def on_delivery_cost_confirm_create(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    price = manager.dialog_data.get("delivery_cost_price")
    free_delivery_amount = manager.dialog_data.get("delivery_cost_free_amount")
    if price is None or free_delivery_amount is None:
        await manager.switch_to(AdminDeliveryPrice.view)
        return

    container = manager.middleware_data["dishka_container"]
    service: DeliveryCostService = await container.get(DeliveryCostService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.create(
            input_dto=CreateDeliveryCost(
                price=price, free_delivery_amount=free_delivery_amount
            )
        )

    await manager.switch_to(AdminDeliveryPrice.view)


async def on_delivery_cost_confirm_update(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    cost_id = manager.dialog_data.get("delivery_cost_id")
    price = manager.dialog_data.get("delivery_cost_price")
    free_delivery_amount = manager.dialog_data.get("delivery_cost_free_amount")
    if not cost_id or price is None or free_delivery_amount is None:
        await manager.switch_to(AdminDeliveryPrice.view)
        return

    container = manager.middleware_data["dishka_container"]
    service: DeliveryCostService = await container.get(DeliveryCostService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.update_by_id(
            input_dto=UpdateDeliveryCost(
                id=UUID(cost_id),
                price=price,
                free_delivery_amount=free_delivery_amount,
            )
        )

    await manager.switch_to(AdminDeliveryPrice.view)


async def on_delivery_cost_cancel(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(AdminDeliveryPrice.view)
