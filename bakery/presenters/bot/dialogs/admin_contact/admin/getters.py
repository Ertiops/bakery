from typing import Any

from aiogram_dialog.api.protocols import DialogManager


async def get_admin_contact_data(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return dialog_manager.start_data  # type: ignore


async def get_admin_contact_preview_data(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, str]:
    return dict(
        name=dialog_manager.dialog_data.get("name", "<нет>"),
        tg_username=dialog_manager.dialog_data.get("tg_username", "<нет>"),
    )
