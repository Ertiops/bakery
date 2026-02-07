from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from bakery.presenters.bot.dialogs.states import UserCatalogue
from bakery.presenters.bot.dialogs.utils.order_edit import get_order_edit_id


async def on_category_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
) -> None:
    order_edit_id = get_order_edit_id(manager)
    admin_order_edit = bool(
        manager.dialog_data.get("admin_order_edit")
        or manager.start_data.get("admin_order_edit")  # type: ignore
    )
    admin_selected_date = (
        manager.dialog_data.get("admin_selected_date")
        or manager.start_data.get("admin_selected_date")  # type: ignore
    )
    admin_deleted_flow = (
        manager.dialog_data.get("admin_deleted_flow")
        if manager.dialog_data.get("admin_deleted_flow") is not None
        else manager.start_data.get("admin_deleted_flow")  # type: ignore
    )
    data: dict[str, Any] = {"category": item_id}
    if order_edit_id:
        data["order_edit_id"] = order_edit_id
    if admin_order_edit:
        data["admin_order_edit"] = True
    if admin_selected_date:
        data["admin_selected_date"] = admin_selected_date
    if admin_deleted_flow is not None:
        data["admin_deleted_flow"] = admin_deleted_flow
    await manager.start(
        state=UserCatalogue.view_products,
        data=data,
    )
