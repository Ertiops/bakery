from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import AdminFakeUsers, UserMain


async def to_main_menu(
    callback: CallbackQuery, button: Button, manager: DialogManager
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
    await manager.done()
    await manager.start(UserMain.menu)
