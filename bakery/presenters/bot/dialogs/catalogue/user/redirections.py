from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import UserCart, UserCatalogue, UserOrder
from bakery.presenters.bot.dialogs.utils.order_edit import get_order_edit_id


async def to_product_categories(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(UserCatalogue.select_category)


async def to_product_list(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    order_edit_id = get_order_edit_id(manager)
    data = dict(category=category)
    if order_edit_id:
        data["order_edit_id"] = order_edit_id
    await manager.start(
        state=UserCatalogue.view_products,
        data=data,
        mode=StartMode.RESET_STACK,
    )


async def to_cart(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.start(
        state=UserCart.view,
        mode=StartMode.RESET_STACK,
    )


async def to_order(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    order_id = get_order_edit_id(manager)
    if not order_id:
        return
    manager.dialog_data["selected_order_id"] = order_id
    await manager.start(
        state=UserOrder.view_one,
        mode=StartMode.RESET_STACK,
        data={"selected_order_id": order_id},
    )
