from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import (
    AdminPickupAddress,
)


async def to_pickup_address_list(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(
        state=AdminPickupAddress.view_all,
    )
