from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import (
    UserCart,
    UserCatalogue,
)


async def enter_catalog(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=UserCatalogue.select_category,
        mode=StartMode.RESET_STACK,
    )


async def enter_cart(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=UserCart.view,
        mode=StartMode.RESET_STACK,
    )
