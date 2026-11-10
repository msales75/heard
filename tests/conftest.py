from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from heard.main import create_app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app = create_app()
    # httpx's ASGITransport doesn't send lifespan events, so run the lifespan here.
    async with (
        app.router.lifespan_context(app),
        AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c,
    ):
        yield c
