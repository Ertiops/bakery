from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import AdminContactTable
from tests.plugins.factories.utils.iteruse import IterUse
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class AdminContactTableFactory(
    SQLAlchemyFactory[AdminContactTable],
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
):
    name = IterUse[str](lambda count: f"test_name_{count}")
    tg_username = IterUse[str](lambda count: f"test_tg_username_{count}")


@pytest.fixture
def create_admin_contact(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> AdminContactTable:
        admin_contact = AdminContactTableFactory.build(**kwargs)
        session.add(admin_contact)
        await session.commit()
        await session.refresh(admin_contact)
        return admin_contact

    return _factory
