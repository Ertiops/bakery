from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import (
    AdminBlacklist,
    AdminCatalogue,
    AdminDeliveryPrice,
    AdminFeedbackGroup,
    AdminOrderPayment,
    AdminOrders,
    AdminOrderSchedule,
    AdminPickupAddress,
)


async def enter_catalog(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=AdminCatalogue.select_category,
        mode=StartMode.RESET_STACK,
    )


async def enter_pickup_address_menu(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=AdminPickupAddress.view_all,
        mode=StartMode.RESET_STACK,
    )


async def enter_delivery_cost(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(AdminDeliveryPrice.view, mode=StartMode.RESET_STACK)


async def to_admin_order_payment(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(state=AdminOrderPayment.view, mode=StartMode.RESET_STACK)


async def to_admin_order_schedule(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(state=AdminOrderSchedule.view, mode=StartMode.RESET_STACK)


async def to_admin_feedback_group(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(state=AdminFeedbackGroup.view, mode=StartMode.RESET_STACK)


async def enter_orders(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(state=AdminOrders.view_categories, mode=StartMode.RESET_STACK)


async def enter_blacklist(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(state=AdminBlacklist.view_list, mode=StartMode.RESET_STACK)
