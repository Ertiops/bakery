from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import OrderTable, UserTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class OrderTableFactory(
    SQLAlchemyFactory[OrderTable], IdentifableFactoryMixin, TimestampedFactoryMixin
):
    pickup_address_id = None


@pytest.fixture
def create_order(
    session: AsyncSession,
    create_user: Callable,
) -> Callable:
    async def _factory(**kwargs) -> OrderTable:
        if kwargs.get("user_id") is None:
            user: UserTable = await create_user()
            kwargs["user_id"] = user.id
        order: OrderTable = OrderTableFactory.build(**kwargs)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order

    return _factory
