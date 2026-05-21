import logging
import sys
from contextvars import ContextVar
from typing import Any

import structlog

from app.core.config import Settings

# Context variable for per-request tracing
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


def _add_request_id(
    logger: Any, method: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    event_dict["request_id"] = request_id_var.get()
    return event_dict


def configure_logging(settings: Settings) -> None:
    """Configure structlog for JSON (production) or pretty console (dev)."""
    shared_processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        _add_request_id,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]

    renderer: structlog.processors.JSONRenderer | structlog.dev.ConsoleRenderer
    if settings.APP_ENV == "production":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Quiet noisy third-party loggers
    for noisy in ("uvicorn.access", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(
            logging.DEBUG if settings.DEBUG else logging.WARNING
        )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Convenience wrapper around structlog.get_logger."""
    return structlog.get_logger(name)
