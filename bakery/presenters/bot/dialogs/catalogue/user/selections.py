from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from bakery.presenters.bot.dialogs.states import UserCatalogue
from bakery.presenters.bot.dialogs.utils.order_edit import get_order_edit_id


async def on_category_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
) -> None:
    order_edit_id = get_order_edit_id(manager)
    data = dict(category=item_id)
    if order_edit_id:
        data["order_edit_id"] = order_edit_id
    await manager.start(
        state=UserCatalogue.view_products,
        data=data,
    )
