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
    container = manager.middleware_data["dishka_container"]
    service: DeliveryCostService = await container.get(DeliveryCostService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.create(input_dto=CreateDeliveryCost(price=value))

    await manager.switch_to(AdminDeliveryPrice.view)


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

    container = manager.middleware_data["dishka_container"]
    service: DeliveryCostService = await container.get(DeliveryCostService)
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.update_by_id(
            input_dto=UpdateDeliveryCost(id=UUID(cost_id), price=value)
        )

    await manager.switch_to(AdminDeliveryPrice.view)
