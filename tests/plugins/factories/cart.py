from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import CartTable, ProductTable, UserTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class CartTableFactory(
    SQLAlchemyFactory[CartTable], IdentifableFactoryMixin, TimestampedFactoryMixin
): ...


@pytest.fixture
def create_cart(
    session: AsyncSession,
    create_user: Callable,
    create_product: Callable,
) -> Callable:
    async def _factory(**kwargs) -> CartTable:
        if kwargs.get("user_id") is None:
            user: UserTable = await create_user()
            kwargs["user_id"] = user.id
        if kwargs.get("product_id") is None:
            product: ProductTable = await create_product()
            kwargs["product_id"] = product.id
        cart: CartTable = CartTableFactory.build(**kwargs)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)
        return cart

    return _factory
