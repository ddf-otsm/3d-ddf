"""Logging configuration for the Logo to 3D service."""

import logging
import sys
from typing import Any, Dict

from structlog import configure, processors, stdlib, threadlocal
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer

from .config import settings


def setup_logging() -> None:
    """Configure structured logging for the application."""

    # Determine log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Shared processors
    shared_processors = [
        stdlib.filter_by_level,
        stdlib.add_logger_name,
        stdlib.add_log_level,
        stdlib.PositionalArgumentsFormatter(),
        threadlocal.merge_threadlocal,
        processors.add_log_level,
        processors.TimeStamper(fmt="iso"),
    ]

    # Choose renderer based on format
    if settings.log_format == "json":
        renderer = JSONRenderer()
    else:
        renderer = ConsoleRenderer(colors=True, pad_event=50)

    # Configure structlog
    configure(
        processors=shared_processors + [
            stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=stdlib.LoggerFactory(),
        wrapper_class=stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure formatter
    formatter = stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=shared_processors,
    )

    # Apply to root logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.WARNING)


def get_logger(name: str) -> Any:
    """Get a structured logger instance."""
    import structlog
    return structlog.get_logger(name)

