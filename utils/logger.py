"""
HackWae Voice Server

Central logging configuration.
"""

from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger

from core.config import settings


def setup_logger() -> None:
    """
    Configure Loguru logger.
    """

    log_dir: Path = settings.paths.logs
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stdout,
        colorize=True,
        level="INFO",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )

    logger.add(
        log_dir / "server.log",
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        level="DEBUG",
        enqueue=True,
    )


setup_logger()
