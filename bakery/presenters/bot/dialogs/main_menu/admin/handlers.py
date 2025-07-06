from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import AdminCatalogue, AdminPickupAddress


async def enter_catalog(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=AdminCatalogue.select_category,
        mode=StartMode.RESET_STACK,
    )


async def enter_pickup_address_menu(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.start(
        state=AdminPickupAddress.view_all,
        mode=StartMode.RESET_STACK,
    )
