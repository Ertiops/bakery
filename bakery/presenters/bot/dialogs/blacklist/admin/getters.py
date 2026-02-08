from typing import Any
from uuid import UUID

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.user import (
    UserBlacklistListParams,
    UserPhoneSearchParams,
)
from bakery.domains.services.user import UserService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.content.messages.blacklist import admin as msg

PAGE_SIZE = 6


async def get_blacklist_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = dialog_manager.middleware_data.get("current_user")
    if current_user is None:
        return dict(has_users=False, users=[], page=0, has_prev=False, has_next=False)

    page = int(dialog_manager.dialog_data.get("blacklist_page", 0))
    async with uow:
        result = await user_service.get_blacklist(
            input_dto=UserBlacklistListParams(
                limit=PAGE_SIZE,
                offset=page * PAGE_SIZE,
            ),
            user=current_user,
        )

    users = [
        dict(id=str(u.id), name=u.name, phone=u.phone, reason=u.exclusion_reason or "")
        for u in result.items
    ]
    has_prev = page > 0
    has_next = result.total > (page + 1) * PAGE_SIZE

    return dict(
        title=msg.LIST_TITLE,
        users=users,
        has_users=bool(users),
        page=page,
        has_prev=has_prev,
        has_next=has_next,
    )


async def get_search_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)
    current_user = dialog_manager.middleware_data.get("current_user")
    if current_user is None:
        return dict(has_users=False, users=[], page=0, has_prev=False, has_next=False)

    query = dialog_manager.dialog_data.get("search_phone") or ""
    page = int(dialog_manager.dialog_data.get("search_page", 0))
    if not query:
        return dict(has_users=False, users=[], page=0, has_prev=False, has_next=False)

    async with uow:
        result = await user_service.search_by_phone(
            input_dto=UserPhoneSearchParams(
                phone=str(query),
                limit=PAGE_SIZE,
                offset=page * PAGE_SIZE,
            ),
            user=current_user,
        )

    users = [
        dict(id=str(u.id), name=u.name, phone=u.phone, reason=u.exclusion_reason or "")
        for u in result.items
    ]
    has_prev = page > 0
    has_next = result.total > (page + 1) * PAGE_SIZE

    return dict(
        title=msg.SEARCH_RESULTS_TITLE,
        users=users,
        has_users=bool(users),
        page=page,
        has_prev=has_prev,
        has_next=has_next,
    )


async def get_blacklist_user_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    user_service: UserService = await container.get(UserService)

    user_id_raw = dialog_manager.dialog_data.get("selected_user_id")
    if not user_id_raw:
        return dict(has_user=False)
    try:
        user_uuid = UUID(user_id_raw)
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
        reason=user.exclusion_reason or "—",
        has_exclusion=bool(user.exclusion_reason),
    )


async def get_blacklist_confirm_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    reason = dialog_manager.dialog_data.get("exclusion_reason") or ""
    return dict(reason=reason)
