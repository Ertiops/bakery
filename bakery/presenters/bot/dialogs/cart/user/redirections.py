from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import UserCatalogue, UserOrder
from bakery.presenters.bot.dialogs.utils.order_for_user import get_order_for_user_data


async def to_product_categories(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(UserCatalogue.select_category)


async def to_product_list(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    data = dict(category=category)
    data.update(get_order_for_user_data(manager))
    await manager.start(
        state=UserCatalogue.view_products,
        data=data,
        mode=StartMode.RESET_STACK,
    )


async def to_order_create(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.start(
        state=UserOrder.add_address,
        mode=StartMode.RESET_STACK,
        data=get_order_for_user_data(manager),
    )
