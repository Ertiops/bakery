from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import OrderPaymentTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class OrderPaymentTableFactory(
    SQLAlchemyFactory[OrderPaymentTable],
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
): ...


@pytest.fixture
def create_order_payment(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> OrderPaymentTable:
        order_payment = OrderPaymentTableFactory.build(**kwargs)
        session.add(order_payment)
        await session.commit()
        await session.refresh(order_payment)
        return order_payment

    return _factory
