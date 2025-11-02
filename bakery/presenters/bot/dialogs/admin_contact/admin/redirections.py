from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import AdminAdminContact


async def to_creation(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminAdminContact.add_name)


async def to_update(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminAdminContact.update_name)
