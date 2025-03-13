FROM python:3.13 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY ./pyproject.toml ./poetry.lock ./
COPY ./infra/bot/supervisord.conf /etc/supervisord.conf

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi &&  \
    poetry add supervisor

FROM python:3.13-slim

RUN useradd --no-create-home appuser
USER appuser

WORKDIR /bot

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

RUN mkdir -p /bot/logs && chown -R appuser:appuser /bot/logs

COPY --chown=appuser:appuser . /bot
