from datetime import date
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bakery.domains.entities.order import CreateOrder, OrderStatus
from bakery.domains.entities.user import User
from bakery.domains.services.order import OrderService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import UserOrder


async def on_address_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["pickup_address_id"] = item_id

    await manager.switch_to(UserOrder.add_date)


async def on_manual_address_entered(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    text = (text or "").strip()
    if not text:
        return

    manager.dialog_data["pickup_address_name"] = text
    manager.dialog_data["has_pickup_address"] = True
    manager.dialog_data.pop("pickup_address_id", None)
    await manager.switch_to(UserOrder.add_date)


async def on_order_date_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    manager.dialog_data["order_date"] = item_id
    await manager.switch_to(UserOrder.confirm)


async def on_confirm_order(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
    **_kwargs: Any,
) -> None:
    container = manager.middleware_data["dishka_container"]
    service: OrderService = await container.get(OrderService)
    user: User = manager.middleware_data["current_user"]
    uow: AbstractUow = await container.get(AbstractUow)

    async with uow:
        await service.create(
            input_dto=CreateOrder(
                user_id=user.id,
                pickup_address_name="pickup_address_name",
                status=OrderStatus.CREATED,
                products=[],
                delivered_at=date.fromisoformat(manager.dialog_data.get("order_date")),  # type: ignore[arg-type]
                price=120,
            )
        )
    await manager.switch_to(UserOrder.finish)
