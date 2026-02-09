from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import OrderTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.services.order import OrderService
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__order_service__hard_delete_list(
    session: AsyncSession,
    order_service: OrderService,
    create_order: Callable,
    create_user: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_order(user_id=(await create_user()).id, deleted_at=old_deleted_at)
    await create_order(user_id=(await create_user()).id, deleted_at=recent_deleted_at)
    await create_order(user_id=(await create_user()).id)

    await order_service.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, OrderTable)
    assert count == 2
