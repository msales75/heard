.PHONY: db fmt check run

# --wait blocks until the Postgres healthcheck passes, so `check` never races startup.
db:
	docker compose up -d --wait db

fmt:
	uv run ruff format .
	uv run ruff check --fix .

# Same steps, same order as .github/workflows/ci.yml.
check: db
	uv run ruff format --check .
	uv run ruff check .
	uv run mypy
	uv run alembic upgrade head
	uv run pytest

run:
	uv run heard
