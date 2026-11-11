import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from heard.config import get_settings
from heard.db import make_engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    engine = make_engine(get_settings().database_url)
    app.state.engine = engine
    try:
        yield
    finally:
        await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="heard", lifespan=lifespan)

    @app.get("/healthz")
    async def healthz(request: Request) -> JSONResponse:
        timeout_s = get_settings().healthz_timeout_s
        engine: AsyncEngine = request.app.state.engine
        try:
            async with asyncio.timeout(timeout_s):
                async with engine.connect() as conn:
                    await conn.execute(text("SELECT 1"))
        except TimeoutError:
            logger.warning("Healthz timeout", extra={"timeout_s": timeout_s})
            return JSONResponse({"status": "error", "database": "timeout"}, status_code=503)
        except Exception:
            logger.exception("health check failed")
            return JSONResponse({"status": "error", "database": "unreachable"}, status_code=503)
        return JSONResponse({"status": "ok", "database": "ok"})

    return app
