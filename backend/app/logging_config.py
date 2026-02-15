import logging
import logging.config
from app.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": settings.LOG_LEVEL,
        }
    },
    "root": {"handlers": ["console"], "level": settings.LOG_LEVEL},
}

def configure_logging() -> None:
    """Configure logging for the application using dictConfig."""
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
    except Exception:
        level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
        logging.basicConfig(level=level)
