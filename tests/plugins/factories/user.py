from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import UserTable
from bakery.domains.entities.user import UserRole
from tests.plugins.factories.utils.iteruse import IterUse
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class UserTableFactory(
    SQLAlchemyFactory[UserTable], IdentifableFactoryMixin, TimestampedFactoryMixin
):
    name = IterUse[str](lambda count: f"test_name_{count}")
    tg_id = IterUse[int](lambda count: count)
    phone = IterUse[str](lambda count: f"+79999999999{count}")
    role: UserRole = UserRole.USER
    exclusion_reason = None


@pytest.fixture
def create_user(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> UserTable:
        user: UserTable = UserTableFactory.build(**kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    return _factory
