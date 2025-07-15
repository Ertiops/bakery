from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog.api.protocols import DialogManager

from bakery.presenters.bot.dialogs.states import UserCatalogue


async def on_view_product_clicked(
    callback: CallbackQuery,
    widget: Any,
    manager: DialogManager,
    item_id: str,
) -> None:
    category = manager.dialog_data.get("category") or manager.start_data.get("category")  # type: ignore
    manager.dialog_data["product_id"] = item_id
    if category:
        manager.dialog_data["category"] = category

    await manager.start(
        state=UserCatalogue.view_single_product,
        data=dict(product_id=item_id, category=category),
    )
