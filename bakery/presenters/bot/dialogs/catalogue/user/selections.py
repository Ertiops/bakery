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
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    admin_order_edit = bool(
        manager.dialog_data.get("admin_order_edit")
        or start_data.get("admin_order_edit")
    )
    admin_selected_date = manager.dialog_data.get(
        "admin_selected_date"
    ) or start_data.get("admin_selected_date")
    admin_deleted_flow = (
        manager.dialog_data.get("admin_deleted_flow")
        if manager.dialog_data.get("admin_deleted_flow") is not None
        else start_data.get("admin_deleted_flow")
    )
    order_for_user_id = manager.dialog_data.get("order_for_user_id") or start_data.get(
        "order_for_user_id"
    )
    admin_fake_user = bool(
        manager.dialog_data.get("admin_fake_user") or start_data.get("admin_fake_user")
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
    if order_for_user_id:
        data["order_for_user_id"] = order_for_user_id
    if admin_fake_user:
        data["admin_fake_user"] = True
    await manager.start(
        state=UserCatalogue.view_products,
        data=data,
    )
