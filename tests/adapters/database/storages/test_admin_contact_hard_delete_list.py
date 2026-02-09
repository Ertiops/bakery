from collections.abc import Callable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import AdminContactTable
from bakery.domains.entities.common import HardDeleteListParams
from bakery.domains.interfaces.storages.admin_contact import IAdminContactStorage
from tests.utils import now_utc


async def _count_rows(session: AsyncSession, table: type) -> int:
    return await session.scalar(select(func.count()).select_from(table)) or 0


async def test__admin_contact_storage__hard_delete_list(
    session: AsyncSession,
    admin_contact_storage: IAdminContactStorage,
    create_admin_contact: Callable,
) -> None:
    old_deleted_at = now_utc(days=-366)
    recent_deleted_at = now_utc(days=-30)
    await create_admin_contact(deleted_at=old_deleted_at)
    await create_admin_contact(deleted_at=recent_deleted_at)
    await create_admin_contact()

    await admin_contact_storage.hard_delete_list(
        input_dto=HardDeleteListParams(deleted_at=old_deleted_at)
    )

    count = await _count_rows(session, AdminContactTable)
    assert count == 2
