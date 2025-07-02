import os
from typing import Any


def format_log(action: str, details: str) -> str:
    """Return a formatted log message."""
    return f"{action}  |  {details}"


def get_logger(base_dir: str) -> dict[str, Any]:
    """Return a logging configuration dictionary.

    Ensures that the logs directory exists and builds a logging config
    compatible with Python's logging module.
    """
    logs_path = os.getenv("LOGGING_DIR", os.path.join(base_dir, "logs"))

    os.makedirs(logs_path, exist_ok=True)

    log_settings = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "lines": {
                "format": (
                    "%(asctime)s %(levelname)-8s [%(name)-12s:%(lineno)d] %(message)s"
                ),
                "datefmt": "%y-%m-%d %H:%M:%S",
            },
            "raw": {
                "format": "%(asctime)s %(message)s",
            },
        },
        "handlers": {
            "console": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "debug": {
                "level": "DEBUG",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": os.path.join(logs_path, "app.log"),
                "formatter": "lines",
            },
            "app_errors": {
                "level": "WARNING",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": os.path.join(logs_path, "app_errors.log"),
                "formatter": "lines",
            },
        },
        "loggers": {
            "config": {
                "handlers": ["debug", "console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "core": {"handlers": ["debug"], "level": "DEBUG", "propagate": True},
            "tg_core": {"handlers": ["debug"], "level": "DEBUG", "propagate": True},
            "profiles": {"handlers": ["debug"], "level": "DEBUG", "propagate": True},
            "": {
                "handlers": ["console", "app_errors"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }

    return log_settings
