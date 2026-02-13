from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import (
    AdminFakeUsers,
    UserCart,
    UserMain,
    UserOrder,
    UserOrderPayment,
)
from bakery.presenters.bot.dialogs.utils.order_for_user import get_order_for_user_data


async def to_cart(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.start(
        state=UserCart.view,
        mode=StartMode.RESET_STACK,
        data=get_order_for_user_data(manager),
    )


async def to_manual_address(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(UserOrder.add_manual_address)


async def to_main_menu_from_order(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    admin_fake_user = bool(
        manager.dialog_data.get("admin_fake_user") or start_data.get("admin_fake_user")
    )
    if admin_fake_user:
        selected_user_id = (
            manager.dialog_data.get("selected_fake_user_id")
            or start_data.get("selected_fake_user_id")
            or manager.dialog_data.get("order_for_user_id")
            or start_data.get("order_for_user_id")
        )
        data = {"selected_fake_user_id": selected_user_id} if selected_user_id else {}
        await manager.start(
            AdminFakeUsers.view_user,
            mode=StartMode.RESET_STACK,
            data=data,
        )
        return
    await manager.start(UserMain.menu, mode=StartMode.RESET_STACK)


async def to_fake_user_card_from_order(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    selected_user_id = (
        manager.dialog_data.get("selected_fake_user_id")
        or start_data.get("selected_fake_user_id")
        or manager.dialog_data.get("order_for_user_id")
        or start_data.get("order_for_user_id")
    )
    data = {"selected_fake_user_id": selected_user_id} if selected_user_id else {}
    await manager.start(
        AdminFakeUsers.view_user,
        mode=StartMode.RESET_STACK,
        data=data,
    )


async def to_order_categories(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(UserOrder.view_categories)


async def to_order_payment(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    order_id = manager.dialog_data.get("selected_order_id")
    if not order_id:
        return

    await manager.start(
        state=UserOrderPayment.show_order_payment,
        mode=StartMode.NORMAL,
        data={"selected_order_id": order_id},
    )


async def to_created_order(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    order_id = manager.dialog_data.get("selected_order_id")
    if not order_id:
        return
    await manager.switch_to(UserOrder.view_one)
