from uuid import UUID

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bakery.application.exceptions import (
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from bakery.domains.entities.user import CreateFakeUser
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.fake_users import admin as msg
from bakery.presenters.bot.dialogs.states import AdminFakeUsers, UserCatalogue

PAGE_SIZE = 6


async def to_fake_users_menu(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["fake_users_page"] = 0
    await manager.switch_to(AdminFakeUsers.view_list)


async def to_fake_users_search(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    await manager.switch_to(AdminFakeUsers.search_phone)


async def on_fake_user_selected(
    callback: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    _ = callback
    _ = widget
    manager.dialog_data["selected_fake_user_id"] = item_id
    await manager.switch_to(AdminFakeUsers.view_user)


async def on_fake_users_next_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["fake_users_page"] = (
        int(manager.dialog_data.get("fake_users_page", 0)) + 1
    )
    await manager.show()


async def on_fake_users_prev_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["fake_users_page"] = max(
        0, int(manager.dialog_data.get("fake_users_page", 0)) - 1
    )
    await manager.show()


async def on_fake_user_name_input(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    _ = message
    _ = widget
    name = (text or "").strip()
    if not name:
        return
    manager.dialog_data["fake_user_name"] = name
    await manager.switch_to(AdminFakeUsers.input_phone)


async def on_fake_user_phone_input(
    message: Message,
    widget: ManagedTextInput[str],
    manager: DialogManager,
    text: str,
) -> None:
    _ = message
    _ = widget
    phone = (text or "").strip()
    if not phone:
        return
    if not phone.isdigit():
        await message.answer(msg.ONLY_DIGITS_ERROR)
        return
    manager.dialog_data["fake_user_phone"] = phone
    await manager.switch_to(AdminFakeUsers.confirm_create)


async def on_fake_user_confirm(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = button
    name = (manager.dialog_data.get("fake_user_name") or "").strip()
    phone = (manager.dialog_data.get("fake_user_phone") or "").strip()
    if not name or not phone:
        return

    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = manager.middleware_data.get("current_user")
    if current_user is None:
        return

    async with uow:
        try:
            await user_service.create_fake_user(
                input_dto=CreateFakeUser(name=name, phone=phone),
                user=current_user,
            )
        except EntityAlreadyExistsException:
            await callback.answer("Пользователь с таким телефоном уже существует.")
            return

    manager.dialog_data.pop("fake_user_name", None)
    manager.dialog_data.pop("fake_user_phone", None)
    manager.dialog_data["fake_users_page"] = 0
    await manager.switch_to(AdminFakeUsers.view_list)


async def on_fake_users_search_input(
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
    if not query.isdigit():
        await message.answer(msg.ONLY_DIGITS_ERROR)
        return
    manager.dialog_data["fake_users_search_phone"] = query
    manager.dialog_data["fake_users_search_page"] = 0
    await manager.switch_to(AdminFakeUsers.view_search)


async def on_fake_users_search_next_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["fake_users_search_page"] = (
        int(manager.dialog_data.get("fake_users_search_page", 0)) + 1
    )
    await manager.show()


async def on_fake_users_search_prev_page(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = callback
    _ = button
    manager.dialog_data["fake_users_search_page"] = max(
        0, int(manager.dialog_data.get("fake_users_search_page", 0)) - 1
    )
    await manager.show()


async def on_create_order_for_fake_user(
    callback: CallbackQuery, button: Button, manager: DialogManager
) -> None:
    _ = button
    user_id_raw = manager.dialog_data.get("selected_fake_user_id")
    if not user_id_raw:
        return
    try:
        user_uuid = UUID(str(user_id_raw))
    except ValueError:
        return

    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    async with uow:
        try:
            await user_service.get_by_id(input_id=user_uuid)
        except EntityNotFoundException:
            return

    await manager.start(
        state=UserCatalogue.select_category,
        mode=StartMode.RESET_STACK,
        data={
            "order_for_user_id": str(user_uuid),
            "admin_fake_user": True,
            "selected_fake_user_id": str(user_uuid),
        },
    )
