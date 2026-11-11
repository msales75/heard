# heard
Extract tasks and facts from conversation

## Development

```sh
cp .env.example .env
docker compose up -d db        # Postgres 16 on localhost:5432
uv sync
uv run alembic upgrade head
uv run heard                   # http://127.0.0.1:8000/healthz
```

Run `make check` before pushing: it starts Postgres and runs the same steps as CI.

Full stack in containers: `docker compose up --build`.

New migration: `uv run alembic revision --autogenerate -m "..."`.
