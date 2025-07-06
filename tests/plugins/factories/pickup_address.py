from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import PickupAddressTable, UserTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class PickupAddressTableFactory(
    SQLAlchemyFactory[PickupAddressTable],
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
): ...


@pytest.fixture
def create_pickup_address(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> UserTable:
        pickup_address: PickupAddressTable = PickupAddressTableFactory.build(**kwargs)
        session.add(pickup_address)
        await session.commit()
        await session.refresh(pickup_address)
        return pickup_address

    return _factory
