from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import OrderScheduleTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class OrderScheduleTableFactory(
    SQLAlchemyFactory[OrderScheduleTable],
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
): ...


@pytest.fixture
def create_order_schedule(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> OrderScheduleTable:
        order_schedule: OrderScheduleTable = OrderScheduleTableFactory.build(**kwargs)
        session.add(order_schedule)
        await session.commit()
        await session.refresh(order_schedule)
        return order_schedule

    return _factory
