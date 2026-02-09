from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import OrderPaymentTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.order_payment import IOrderPaymentStorage
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__order_payment_storage__hard_delete_list(
    session: AsyncSession,
    order_payment_storage: IOrderPaymentStorage,
    create_order_payment: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_order_payment(deleted_at=old_deleted_at)
    await create_order_payment(deleted_at=recent_deleted_at)
    await create_order_payment()

    await order_payment_storage.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, OrderPaymentTable)
    assert count == 2
