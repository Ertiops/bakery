from typing import Any
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.user import UserFakeListParams, UserFakeSearchParams
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.fake_users.admin.handlers import PAGE_SIZE


async def get_fake_users_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = dialog_manager.middleware_data.get("current_user")
    if current_user is None:
        return dict(users=[], has_users=False)

    page = int(dialog_manager.dialog_data.get("fake_users_page", 0))
    offset = page * PAGE_SIZE

    async with uow:
        result = await user_service.get_fake_users(
            input_dto=UserFakeListParams(limit=PAGE_SIZE, offset=offset),
            user=current_user,
        )

    users = [dict(id=str(u.id), name=u.name, phone=u.phone) for u in result.items]
    total = result.total
    has_prev = page > 0
    has_next = offset + PAGE_SIZE < total

    return dict(
        users=users,
        has_users=bool(users),
        has_prev=has_prev,
        has_next=has_next,
    )


async def get_fake_user_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)

    user_id_raw = dialog_manager.dialog_data.get("selected_fake_user_id")
    if user_id_raw is None and isinstance(dialog_manager.start_data, dict):
        user_id_raw = dialog_manager.start_data.get("selected_fake_user_id")
        if user_id_raw:
            dialog_manager.dialog_data["selected_fake_user_id"] = user_id_raw
    if not user_id_raw:
        return dict(has_user=False)
    try:
        user_uuid = UUID(str(user_id_raw))
    except ValueError:
        return dict(has_user=False)

    async with uow:
        try:
            user = await user_service.get_by_id(input_id=user_uuid)
        except EntityNotFoundException:
            return dict(has_user=False)

    return dict(
        has_user=True,
        name=user.name,
        phone=user.phone,
    )


async def get_fake_users_search_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = dialog_manager.middleware_data.get("current_user")
    if current_user is None:
        return dict(users=[], has_users=False)

    query = (dialog_manager.dialog_data.get("fake_users_search_phone") or "").strip()
    page = int(dialog_manager.dialog_data.get("fake_users_search_page", 0))
    offset = page * PAGE_SIZE

    async with uow:
        result = await user_service.search_fake_users_by_phone(
            input_dto=UserFakeSearchParams(
                phone=query,
                limit=PAGE_SIZE,
                offset=offset,
            ),
            user=current_user,
        )

    users = [dict(id=str(u.id), name=u.name, phone=u.phone) for u in result.items]
    total = result.total
    has_prev = page > 0
    has_next = offset + PAGE_SIZE < total

    return dict(
        users=users,
        has_users=bool(users),
        has_prev=has_prev,
        has_next=has_next,
    )


async def get_fake_user_confirm_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    name = dialog_manager.dialog_data.get("fake_user_name") or ""
    phone = dialog_manager.dialog_data.get("fake_user_phone") or ""
    return dict(
        name=name,
        phone=phone,
        has_data=bool(name and phone),
    )
