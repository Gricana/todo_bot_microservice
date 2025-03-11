FROM python:3.13 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

WORKDIR /comments_api

COPY ./pyproject.toml ./poetry.lock ./
COPY ./infra/api/supervisord.conf /etc/supervisord.conf

RUN poetry config virtualenvs.create false &&  \
    poetry install --no-interaction --no-ansi &&  \
    poetry add supervisor

FROM python:3.13-slim

WORKDIR /comments_api

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

RUN mkdir -p /comments_api/logs

COPY . /comments_api

EXPOSE 8090
