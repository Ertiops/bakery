from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import UserMain


async def to_main_menu(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.done()
    await manager.start(UserMain.menu)
