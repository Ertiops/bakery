from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import FeedbackGroupTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.feedback_group import IFeedbackGroupStorage
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__feedback_group_storage__hard_delete_list(
    session: AsyncSession,
    feedback_group_storage: IFeedbackGroupStorage,
    create_feedback_group: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_feedback_group(deleted_at=old_deleted_at)
    await create_feedback_group(deleted_at=recent_deleted_at)
    await create_feedback_group()

    await feedback_group_storage.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, FeedbackGroupTable)
    assert count == 2
