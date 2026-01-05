from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import DeliveryCostTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class DeliveryCostTableFactory(
    SQLAlchemyFactory[DeliveryCostTable],
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
): ...


@pytest.fixture
def create_delivery_cost(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> DeliveryCostTable:
        delivery_cost = DeliveryCostTableFactory.build(**kwargs)
        session.add(delivery_cost)
        await session.commit()
        await session.refresh(delivery_cost)
        return delivery_cost

    return _factory
