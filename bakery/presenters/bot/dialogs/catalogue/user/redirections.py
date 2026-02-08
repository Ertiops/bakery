from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.domains.entities.user import UserRole
from bakery.presenters.bot.dialogs.main_menu.user.redirections import to_main_menu
from bakery.presenters.bot.dialogs.states import (
    AdminOrders,
    UserCart,
    UserCatalogue,
    UserOrder,
)
from bakery.presenters.bot.dialogs.utils.order_edit import get_order_edit_id


async def to_product_categories(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(UserCatalogue.select_category)


async def to_product_list(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    category = manager.dialog_data.get("category") or start_data.get("category")
    order_edit_id = get_order_edit_id(manager)
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
    data = dict(category=category)
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
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    current_user = manager.middleware_data.get("current_user")
    is_admin = bool(current_user and current_user.role == UserRole.ADMIN)
    manager.dialog_data["selected_order_id"] = order_id
    admin_selected_date = manager.dialog_data.get(
        "admin_selected_date"
    ) or start_data.get("admin_selected_date")
    admin_deleted_flow = (
        manager.dialog_data.get("admin_deleted_flow")
        if manager.dialog_data.get("admin_deleted_flow") is not None
        else start_data.get("admin_deleted_flow")
    )
    if (
        manager.dialog_data.get("admin_order_edit")
        or start_data.get("admin_order_edit")
        or is_admin
    ):
        await manager.start(
            state=AdminOrders.view_user_order,
            mode=StartMode.RESET_STACK,
            data={
                "selected_order_id": order_id,
                "admin_selected_date": admin_selected_date,
                "admin_deleted_flow": admin_deleted_flow,
            },
        )
    else:
        await manager.start(
            state=UserOrder.view_one,
            mode=StartMode.RESET_STACK,
            data={"selected_order_id": order_id},
        )


async def to_catalogue_root(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    order_id = get_order_edit_id(manager)
    start_data = manager.start_data if isinstance(manager.start_data, dict) else {}
    current_user = manager.middleware_data.get("current_user")
    is_admin = bool(current_user and current_user.role == UserRole.ADMIN)
    admin_selected_date = manager.dialog_data.get(
        "admin_selected_date"
    ) or start_data.get("admin_selected_date")
    admin_deleted_flow = (
        manager.dialog_data.get("admin_deleted_flow")
        if manager.dialog_data.get("admin_deleted_flow") is not None
        else start_data.get("admin_deleted_flow")
    )
    if (
        manager.dialog_data.get("admin_order_edit")
        or start_data.get("admin_order_edit")
        or is_admin
    ) and order_id:
        manager.dialog_data["selected_order_id"] = order_id
        await manager.start(
            state=AdminOrders.view_user_order,
            mode=StartMode.RESET_STACK,
            data={
                "selected_order_id": order_id,
                "admin_selected_date": admin_selected_date,
                "admin_deleted_flow": admin_deleted_flow,
            },
        )
        return
    await to_main_menu(callback, button, manager)
