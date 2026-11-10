import uvicorn

from heard.config import get_settings
from heard.log import configure_logging


def main() -> None:
    settings = get_settings()
    configure_logging(settings.log_level)
    # log_config=None stops uvicorn installing its own handlers, so its
    # loggers propagate to our root JSON handler.
    uvicorn.run(
        "heard.main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        log_config=None,
    )


if __name__ == "__main__":
    main()
