import asyncio
import time
from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager
from typing import NoReturn

import pytest
from httpx import ASGITransport, AsyncClient

from heard.config import get_settings
from heard.main import create_app


async def test_healthz_reports_database_ok(client: AsyncClient) -> None:
    resp = await client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "database": "ok"}


class HangingEngine:
    """Stands in for AsyncEngine; connect() never completes."""

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[NoReturn]:
        await asyncio.get_running_loop().create_future()  # never resolved
        raise AssertionError("unreachable")
        yield


@pytest.fixture
def short_healthz_timeout(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("HEALTHZ_TIMEOUT_S", "0.1")
    get_settings.cache_clear()
    yield
    # Runs before monkeypatch restores the env, so the next get_settings() call
    # re-reads the real environment instead of reusing the 0.1s settings.
    get_settings.cache_clear()


@pytest.mark.usefixtures("short_healthz_timeout")
async def test_healthz_times_out_when_database_hangs() -> None:
    assert get_settings().healthz_timeout_s == 0.1

    app = create_app()  # lifespan deliberately not run: no real engine is created
    app.state.engine = HangingEngine()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        start = time.monotonic()
        resp = await c.get("/healthz")
        elapsed = time.monotonic() - start

    assert resp.status_code == 503
    assert resp.json() == {"status": "error", "database": "timeout"}
    assert elapsed < 1.0
