from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import PickupAddressTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.pickup_address import IPickupAddressStorage
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__pickup_address_storage__hard_delete_list(
    session: AsyncSession,
    pickup_address_storage: IPickupAddressStorage,
    create_pickup_address: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_pickup_address(deleted_at=old_deleted_at)
    await create_pickup_address(deleted_at=recent_deleted_at)
    await create_pickup_address()

    await pickup_address_storage.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, PickupAddressTable)
    assert count == 2
