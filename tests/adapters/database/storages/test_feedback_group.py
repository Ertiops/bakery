from collections.abc import Awaitable, Callable
from datetime import timedelta
from uuid import uuid4

import pytest
from dirty_equals import IsDatetime, IsUUID

from bakery.adapters.database.storages.feedback_group import FeedbackGroupStorage
from bakery.adapters.database.tables import FeedbackGroupTable
from bakery.application.exceptions import EntityNotFoundException
from bakery.domains.entities.feedback_group import (
    CreateFeedbackGroup,
    FeedbackGroup,
    UpdateFeedbackGroup,
)
from tests.utils import now_utc


async def test__create(
    feedback_group_storage: FeedbackGroupStorage,
) -> None:
    create_data = CreateFeedbackGroup(url="https://t.me/test")
    feedback_group = await feedback_group_storage.create(input_dto=create_data)
    assert feedback_group == FeedbackGroup(
        id=IsUUID,
        url=create_data.url,
        created_at=IsDatetime,
        updated_at=IsDatetime,
    )


async def test__get_last(
    feedback_group_storage: FeedbackGroupStorage,
    create_feedback_group: Callable,
) -> None:
    db_feedback_group: FeedbackGroupTable = await create_feedback_group()
    await create_feedback_group(created_at=now_utc() - timedelta(days=1))
    feedback_group = await feedback_group_storage.get_last()
    assert feedback_group == FeedbackGroup(
        id=db_feedback_group.id,
        url=db_feedback_group.url,
        created_at=db_feedback_group.created_at,
        updated_at=db_feedback_group.updated_at,
    )


async def test__get_last__none(
    feedback_group_storage: FeedbackGroupStorage,
) -> None:
    assert await feedback_group_storage.get_last() is None


async def test__update_by_id(
    feedback_group_storage: FeedbackGroupStorage,
    create_feedback_group: Callable[..., Awaitable[FeedbackGroupTable]],
) -> None:
    db_feedback_group = await create_feedback_group()
    update_data = UpdateFeedbackGroup(
        id=db_feedback_group.id,
        url="https://t.me/updated",
    )
    feedback_group = await feedback_group_storage.update_by_id(input_dto=update_data)
    assert feedback_group == FeedbackGroup(
        id=db_feedback_group.id,
        url=update_data.url,
        created_at=db_feedback_group.created_at,
        updated_at=IsDatetime,
    )


async def test__update_by_id__entity_not_found_exception(
    feedback_group_storage: FeedbackGroupStorage,
) -> None:
    with pytest.raises(EntityNotFoundException):
        await feedback_group_storage.update_by_id(
            input_dto=UpdateFeedbackGroup(
                id=uuid4(),
            )
        )
