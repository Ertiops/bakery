from uuid import UUID

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bakery.application.entities import Unset
from bakery.domains.entities.feedback_group import (
    CreateFeedbackGroup,
    UpdateFeedbackGroup,
)
from bakery.domains.services.feedback_group import FeedbackGroupService
from bakery.domains.uow import AbstractUow
from bakery.presenters.bot.dialogs.states import AdminFeedbackGroup
from bakery.presenters.bot.utils.text import UNSET_MARK, extract_text, normalize_text


async def admin_feedback_group_start_create(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["feedback_group_mode"] = "create"
    manager.dialog_data.pop("feedback_group_id", None)
    manager.dialog_data.pop("feedback_group_url_value", None)
    manager.dialog_data.pop("feedback_group_original_url_value", None)

    await manager.switch_to(AdminFeedbackGroup.url)


async def admin_feedback_group_start_update(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: FeedbackGroupService = await container.get(FeedbackGroupService)

    async with uow:
        feedback_group = await service.get_last()

    manager.dialog_data["feedback_group_mode"] = "update"
    manager.dialog_data["feedback_group_id"] = str(feedback_group.id)
    manager.dialog_data["feedback_group_url_value"] = feedback_group.url
    manager.dialog_data["feedback_group_original_url_value"] = feedback_group.url

    await manager.switch_to(AdminFeedbackGroup.url)


async def admin_feedback_group_back_to_view(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(AdminFeedbackGroup.view)


async def admin_feedback_group_on_url_input(
    message: Message,
    _widget: object,
    manager: DialogManager,
) -> None:
    if message.content_type != ContentType.TEXT:
        return
    value = normalize_text(message.text)
    if not value:
        return
    manager.dialog_data["feedback_group_url_value"] = value
    await manager.switch_to(AdminFeedbackGroup.confirm)


async def admin_feedback_group_skip_url_input(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    manager.dialog_data["feedback_group_url_value"] = UNSET_MARK
    await manager.switch_to(AdminFeedbackGroup.confirm)


async def admin_feedback_group_save(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
) -> None:
    container = manager.middleware_data["dishka_container"]
    uow: AbstractUow = await container.get(AbstractUow)
    service: FeedbackGroupService = await container.get(FeedbackGroupService)

    mode = manager.dialog_data.get("feedback_group_mode", "create")

    async with uow:
        if mode == "update":
            url = extract_text(manager.dialog_data.get("feedback_group_url_value"))
            if isinstance(url, Unset):
                url = normalize_text(
                    manager.dialog_data.get("feedback_group_original_url_value")
                )
            feedback_group_id = manager.dialog_data.get("feedback_group_id")
            if not feedback_group_id:
                return
            await service.update_by_id(
                input_dto=UpdateFeedbackGroup(
                    id=UUID(feedback_group_id),
                    url=url,
                )
            )
        else:
            url = normalize_text(manager.dialog_data.get("feedback_group_url_value"))
            if not url:
                return
            await service.create(input_dto=CreateFeedbackGroup(url=url))

    await manager.switch_to(AdminFeedbackGroup.view)
