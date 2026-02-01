from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import ProductTable, UserTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class ProductTableFactory(
    SQLAlchemyFactory[ProductTable], IdentifableFactoryMixin, TimestampedFactoryMixin
):
    photo_file_id = "photo_file_id"


@pytest.fixture
def create_product(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> UserTable:
        product: ProductTable = ProductTableFactory.build(**kwargs)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    return _factory
