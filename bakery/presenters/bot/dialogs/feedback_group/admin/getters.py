from typing import Any

from aiogram_dialog.api.protocols import DialogManager

from bakery.application.entities import Unset
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.services.feedback_group import FeedbackGroupService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.utils.text import UNSET_MARK, display_text


async def get_admin_feedback_group_view_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    container = dialog_manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: FeedbackGroupService = await container.get(FeedbackGroupService)

    async with uow:
        try:
            feedback_group = await service.get_last()
        except EntityNotFoundException:
            return dict(has_feedback_group=False, feedback_group_id=None, url="")

    return dict(
        has_feedback_group=True,
        feedback_group_id=str(feedback_group.id),
        url=feedback_group.url,
    )


async def get_admin_feedback_group_edit_data(
    dialog_manager: DialogManager,
    **_kwargs: Any,
) -> dict[str, Any]:
    return dict(
        mode=dialog_manager.dialog_data.get("feedback_group_mode", "create"),
        is_update=dialog_manager.dialog_data.get("feedback_group_mode") == "update",
        feedback_group_id=dialog_manager.dialog_data.get("feedback_group_id"),
        url=_resolve_value(
            dialog_manager.dialog_data.get("feedback_group_url_value"),
            dialog_manager.dialog_data.get("feedback_group_original_url_value"),
        ),
        has_url=_has_value(
            dialog_manager.dialog_data.get("feedback_group_url_value"),
            dialog_manager.dialog_data.get("feedback_group_original_url_value"),
        ),
    )


def _resolve_value(value: str | Unset | None, original: str | None) -> str:
    if value == UNSET_MARK:
        return display_text(original)
    return display_text(value)


def _has_value(value: object, original: object) -> bool:
    if value == UNSET_MARK:
        return bool(original)
    return bool(value) and not isinstance(value, Unset) and value != UNSET_MARK
