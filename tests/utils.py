from collections.abc import Sequence
from datetime import UTC, datetime

from alembic.autogenerate import compare_metadata
from alembic.config import Config as AlembicConfig
from alembic.runtime.environment import EnvironmentContext
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import Connection, MetaData, pool, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_engine_from_config,
)

TABLES_FOR_TRUNCATE: Sequence[str] = (
    "users",
    "products",
    "orders",
    "pickup_addresses",
    "user_addresses",
)
TYPES_FOR_TRUNCATE: Sequence[str] = ("product_category", "order_status")


async def truncate_tables(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for table in TABLES_FOR_TRUNCATE:
            await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
        await conn.commit()


async def truncate_types(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for type_name in TYPES_FOR_TRUNCATE:
            await conn.execute(text(f"DROP TYPE IF EXISTS {type_name} CASCADE"))


async def run_async_migrations(
    config: AlembicConfig,
    target_metadata: MetaData,
    revision: str,
) -> None:
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs(revision, rev)

    with EnvironmentContext(
        config,
        script=script,
        fn=upgrade,
        as_sql=False,
        starting_rev=None,
        destination_rev=revision,
    ) as context:
        engine = async_engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )
        async with engine.connect() as connection:
            await connection.run_sync(
                _do_run_migrations,
                target_metadata=target_metadata,
                context=context,
            )


def _do_run_migrations(
    connection: Connection,
    target_metadata: MetaData,
    context: EnvironmentContext,
) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def get_diff_db_metadata(connection: Connection, metadata: MetaData):
    migration_ctx = MigrationContext.configure(connection)
    return compare_metadata(context=migration_ctx, metadata=metadata)


def now_utc() -> datetime:
    return datetime.now(tz=UTC)
