from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import DeliveryCostTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.delivery_cost import IDeliveryCostStorage
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__delivery_cost_storage__hard_delete_list(
    session: AsyncSession,
    delivery_cost_storage: IDeliveryCostStorage,
    create_delivery_cost: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_delivery_cost(deleted_at=old_deleted_at)
    await create_delivery_cost(deleted_at=recent_deleted_at)
    await create_delivery_cost()

    await delivery_cost_storage.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, DeliveryCostTable)
    assert count == 2
