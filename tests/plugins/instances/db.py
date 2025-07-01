from collections.abc import AsyncIterator
from types import SimpleNamespace

import pytest
from alembic.config import Config as AlembicConfig
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from bakery.adapters.database.config import DatabaseConfig
from bakery.adapters.database.tables import BaseTable
from bakery.adapters.database.utils import (
    create_engine,
    create_sessionmaker,
    make_alembic_config,
)
from tests.utils import run_async_migrations, truncate_tables


@pytest.fixture
def db_config() -> DatabaseConfig:
    return DatabaseConfig()


@pytest.fixture
def alembic_config(db_config: DatabaseConfig) -> AlembicConfig:
    cmd_options = SimpleNamespace(
        config="alembic.ini",
        name="alembic",
        raiseerr=False,
        x=None,
    )
    return make_alembic_config(cmd_options, pg_url=db_config.dsn)


@pytest.fixture
async def engine(
    alembic_config: AlembicConfig,
    db_config: DatabaseConfig,
) -> AsyncIterator[AsyncEngine]:
    await run_async_migrations(alembic_config, BaseTable.metadata, "head")
    async with create_engine(dsn=db_config.dsn, debug=True) as engine:
        await truncate_tables(engine)
        yield engine


@pytest.fixture
def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return create_sessionmaker(engine=engine)


@pytest.fixture
async def session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
        await session.rollback()
