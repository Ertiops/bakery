from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import AdminCatalogue


async def enter_catalog(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(AdminCatalogue.select_category)
