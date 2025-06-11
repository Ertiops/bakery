from collections.abc import Callable
from datetime import datetime

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import ProductTable, UserTable
from tests.utils import now_utc


class ProductTableFactory(SQLAlchemyFactory[ProductTable]):
    @classmethod
    def created_at(cls) -> datetime:
        return now_utc()

    @classmethod
    def deleted_at(cls) -> None:
        return None


@pytest.fixture
def create_product(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> UserTable:
        product: ProductTable = ProductTableFactory.build(**kwargs)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    return _factory
