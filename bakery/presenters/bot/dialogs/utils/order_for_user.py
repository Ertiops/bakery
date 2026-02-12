from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.domains.entities.user import User


def get_order_for_user_id(dialog_manager: DialogManager) -> UUID:
    raw = dialog_manager.dialog_data.get("order_for_user_id")
    if raw is None and isinstance(dialog_manager.start_data, dict):
        raw = dialog_manager.start_data.get("order_for_user_id")
    if raw:
        try:
            return UUID(str(raw))
        except ValueError:
            pass
    user: User = dialog_manager.middleware_data["current_user"]
    return user.id


def get_order_for_user_data(dialog_manager: DialogManager) -> dict[str, object]:
    data: dict[str, object] = {}
    raw = dialog_manager.dialog_data.get("order_for_user_id")
    if raw is None and isinstance(dialog_manager.start_data, dict):
        raw = dialog_manager.start_data.get("order_for_user_id")
    if raw:
        data["order_for_user_id"] = raw
    selected_fake_user_id = dialog_manager.dialog_data.get("selected_fake_user_id")
    if selected_fake_user_id is None and isinstance(dialog_manager.start_data, dict):
        selected_fake_user_id = dialog_manager.start_data.get("selected_fake_user_id")
    if selected_fake_user_id:
        data["selected_fake_user_id"] = selected_fake_user_id
    admin_fake_user = dialog_manager.dialog_data.get("admin_fake_user")
    if admin_fake_user is None and isinstance(dialog_manager.start_data, dict):
        admin_fake_user = dialog_manager.start_data.get("admin_fake_user")
    if admin_fake_user:
        data["admin_fake_user"] = True
    return data
