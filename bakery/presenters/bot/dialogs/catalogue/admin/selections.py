from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from bakery.presenters.bot.dialogs.states import (
    AdminCatalogue,
)


async def on_category_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
) -> None:
    await manager.start(
        state=AdminCatalogue.view_products,
        data={"category": item_id},
    )
