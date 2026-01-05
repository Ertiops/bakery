from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import AdminMain


async def to_admin_main_menu(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(AdminMain.menu, mode=StartMode.RESET_STACK)
