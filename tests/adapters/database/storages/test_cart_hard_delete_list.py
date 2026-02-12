from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import CartTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.cart import ICartStorage
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__cart_storage__hard_delete_list(
    session: AsyncSession,
    cart_storage: ICartStorage,
    create_cart: Callable,
    create_user: Callable,
    create_product: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    old_user = await create_user()
    old_product = await create_product()
    recent_user = await create_user()
    recent_product = await create_product()
    fresh_user = await create_user()
    fresh_product = await create_product()
    await create_cart(
        user_id=old_user.id,
        product_id=old_product.id,
        deleted_at=old_deleted_at,
    )
    await create_cart(
        user_id=recent_user.id,
        product_id=recent_product.id,
        deleted_at=recent_deleted_at,
    )
    await create_cart(user_id=fresh_user.id, product_id=fresh_product.id)

    await cart_storage.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, CartTable)
    assert count == 2
