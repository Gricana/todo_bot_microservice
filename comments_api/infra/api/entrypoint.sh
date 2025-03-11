#!/bin/bash
set -e

./infra/db/wait-for-it.sh db:5432 -- echo "Database is up"

export PYTHONPATH=/comments_api:$PYTHONPATH

if [ ! -d "migrations" ]; then
    alembic init migrations
    sed -i "s|sqlalchemy.url = .*|sqlalchemy.url = postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}|" alembic.ini
    alembic revision --autogenerate -m "Initial migration"
fi

alembic upgrade head

supervisord -c /etc/supervisord.conf
