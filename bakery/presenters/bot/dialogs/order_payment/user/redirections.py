from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import (
    UserOrder,
)


async def to_order_categories(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=UserOrder.view_categories,
        mode=StartMode.NORMAL,
    )
