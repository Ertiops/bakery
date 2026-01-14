from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import UserCart, UserMain, UserOrder


async def to_cart(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.start(
        state=UserCart.view,
        mode=StartMode.RESET_STACK,
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
    await manager.start(UserMain.menu, mode=StartMode.RESET_STACK)


async def to_order_categories(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(UserOrder.view_categories)


async def to_payment_stub(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await callback.answer(
        "🧾 Заглушка: здесь будет переход на оплату заказа", show_alert=True
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
