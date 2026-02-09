from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import ProductTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.services.product import ProductService
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__product_service__hard_delete_list(
    session: AsyncSession,
    product_service: ProductService,
    create_product: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_product(deleted_at=old_deleted_at)
    await create_product(deleted_at=recent_deleted_at)
    await create_product()

    await product_service.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, ProductTable)
    assert count == 2
