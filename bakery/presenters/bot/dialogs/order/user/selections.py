from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.order import UserOrderStatus
from bakery.presenters.bot.dialogs.states import UserOrder


async def select_orders_cat_created(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["user_order_status"] = UserOrderStatus.CREATED.value
    manager.dialog_data["orders_page"] = 0
    await manager.switch_to(UserOrder.view_many)


async def select_orders_cat_delivered(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["user_order_status"] = UserOrderStatus.DELIVERED.value
    manager.dialog_data["orders_page"] = 0
    await manager.switch_to(UserOrder.view_many)


async def select_orders_cat_paid(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["user_order_status"] = UserOrderStatus.PAID.value
    manager.dialog_data["orders_page"] = 0
    await manager.switch_to(UserOrder.view_many)
