from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.user import UserClearExclusionParams, UserExclusionParams
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminBlacklist

PAGE_SIZE = 6


async def to_blacklist_menu(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["blacklist_page"] = 0
    await manager.switch_to(AdminBlacklist.view_list)


async def to_search_phone(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    await manager.switch_to(AdminBlacklist.search_phone)


async def on_search_phone_input(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    _ = message
    _ = widget
    query = (text or "").strip()
    if not query:
        return
    manager.dialog_data["search_phone"] = query
    manager.dialog_data["search_page"] = 0
    await manager.switch_to(AdminBlacklist.view_search)


async def on_blacklist_user_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    _ = callback
    _ = widget
    manager.dialog_data["selected_user_id"] = item_id
    await manager.switch_to(AdminBlacklist.view_user)


async def on_blacklist_next_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["blacklist_page"] = (
        int(manager.dialog_data.get("blacklist_page", 0)) + 1
    )
    await manager.show()


async def on_blacklist_prev_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["blacklist_page"] = max(
        0, int(manager.dialog_data.get("blacklist_page", 0)) - 1
    )
    await manager.show()


async def on_search_next_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["search_page"] = (
        int(manager.dialog_data.get("search_page", 0)) + 1
    )
    await manager.show()


async def on_search_prev_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["search_page"] = max(
        0, int(manager.dialog_data.get("search_page", 0)) - 1
    )
    await manager.show()


async def on_blacklist_add_start(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    await manager.switch_to(AdminBlacklist.input_reason)


async def on_blacklist_reason_input(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    _ = message
    _ = widget
    reason = (text or "").strip()
    if not reason:
        return
    manager.dialog_data["exclusion_reason"] = reason
    await manager.switch_to(AdminBlacklist.confirm_add)


async def on_blacklist_confirm(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = button
    user_id_raw = manager.dialog_data.get("selected_user_id")
    reason = (manager.dialog_data.get("exclusion_reason") or "").strip()
    if not user_id_raw or not reason:
        return
    try:
        user_uuid = UUID(str(user_id_raw))
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    async with uow:
        try:
            await user_service.set_exclusion_reason(
                input_dto=UserExclusionParams(id=user_uuid, reason=reason),
                user=current_user,
            )
        except EntityNotFoundException:
            return

    manager.dialog_data.pop("exclusion_reason", None)
    await manager.switch_to(AdminBlacklist.view_list)


async def on_blacklist_remove(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = button
    user_id_raw = manager.dialog_data.get("selected_user_id")
    if not user_id_raw:
        return
    try:
        user_uuid = UUID(str(user_id_raw))
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    async with uow:
        try:
            await user_service.clear_exclusion_reason(
                input_dto=UserClearExclusionParams(id=user_uuid),
                user=current_user,
            )
        except EntityNotFoundException:
            return

    await manager.switch_to(AdminBlacklist.view_list)
