import logging
import sys
from typing import Literal

LogLevel = Literal["debug", "info", "warning", "error"]

_LEVEL_MAP: dict[LogLevel, int] = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


def setup_logging(level: LogLevel = "info") -> None:
    """Configure application-wide logging. Safe to call multiple times."""
    root = logging.getLogger()
    if root.handlers:
        root.setLevel(_LEVEL_MAP[level])
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
    )

    root.setLevel(_LEVEL_MAP[level])
    root.addHandler(handler)

    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
