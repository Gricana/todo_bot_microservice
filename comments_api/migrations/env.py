from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from models.comment import Base
from settings import settings

# Получаем конфигурацию Alembic
config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Настройка логирования, если указано в конфиге
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные моделей для автогенерации
target_metadata = Base.metadata

# Асинхронный движок SQLAlchemy
connectable = create_async_engine(settings.DATABASE_URL, echo=True)


async def run_migrations_online():
    """Запускаем миграции в онлайн-режиме с асинхронным подключением."""
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Настраиваем контекст и запускаем миграции."""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline():
    """Запускаем миграции в оффлайн-режиме."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# Определяем режим работы: онлайн или оффлайн
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
