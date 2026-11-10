import asyncio

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

from heard.config import get_settings
from heard.db import Base
from heard.log import configure_logging

config = context.config
settings = get_settings()
# Same JSON logging as the app; the [logger_*] sections in alembic.ini are unused.
configure_logging(settings.log_level)

target_metadata = Base.metadata
# Read the URL from app settings rather than alembic.ini so there is one source of
# truth (and no ConfigParser %-escaping of passwords).
database_url = settings.database_url


def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    engine = create_async_engine(database_url, poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())
