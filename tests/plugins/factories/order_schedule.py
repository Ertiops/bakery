from collections.abc import Callable
from datetime import time

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
):
    weekdays = [1, 2, 3, 4, 5, 6, 7]
    min_days_before = 0
    max_days_in_advance = 0
    order_open_time = time(21, 0)
    order_close_time = time(20, 59)


@pytest.fixture
def create_order_schedule(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> OrderScheduleTable:
        order_schedule: OrderScheduleTable = OrderScheduleTableFactory.build(**kwargs)
        session.add(order_schedule)
        await session.commit()
        await session.refresh(order_schedule)
        return order_schedule

    return _factory
