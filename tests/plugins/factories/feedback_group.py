from collections.abc import Callable

import pytest
from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from sqlalchemy.ext.asyncio import AsyncSession

from bakery.adapters.database.tables import FeedbackGroupTable
from tests.plugins.factories.utils.mixins import (
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
)


class FeedbackGroupTableFactory(
    SQLAlchemyFactory[FeedbackGroupTable],
    IdentifableFactoryMixin,
    TimestampedFactoryMixin,
):
    url = "https://t.me/test"


@pytest.fixture
def create_feedback_group(session: AsyncSession) -> Callable:
    async def _factory(**kwargs) -> FeedbackGroupTable:
        feedback_group = FeedbackGroupTableFactory.build(**kwargs)
        session.add(feedback_group)
        await session.commit()
        await session.refresh(feedback_group)
        return feedback_group

    return _factory
