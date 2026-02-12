from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import OrderScheduleTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.services.order_schedule import OrderScheduleService
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__order_schedule_service__hard_delete_list(
    session: AsyncSession,
    order_schedule_service: OrderScheduleService,
    create_order_schedule: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_order_schedule(deleted_at=old_deleted_at)
    await create_order_schedule(deleted_at=recent_deleted_at)
    await create_order_schedule()

    await order_schedule_service.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, OrderScheduleTable)
    assert count == 2
