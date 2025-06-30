from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import StartMode
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.presenters.bot.dialogs.states import AdminCatalogue, AdminMain


async def to_product_categories(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.switch_to(AdminCatalogue.select_category)


async def to_product_list(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    await manager.start(
        state=AdminCatalogue.view_products,
        data={"category": category},
        mode=StartMode.RESET_STACK,
    )


async def to_main_menu(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    await manager.done()
    await manager.start(AdminMain.menu)
