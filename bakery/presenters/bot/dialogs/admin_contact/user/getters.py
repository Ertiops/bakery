from typing import Any

from aiogram_dialog.api.protocols import DialogManager


async def get_admin_contact_data(
    dialog_manager: DialogManager, **kwargs: Any
) -> dict[str, Any]:
    return dialog_manager.start_data  # type: ignore
