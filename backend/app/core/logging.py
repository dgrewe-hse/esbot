"""Logging configuration for the ESBot backend."""

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    """Configure application-wide logging."""
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
