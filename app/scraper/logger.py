"""Logging setup for the scraper module."""

import io
import logging

logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)

_formatter = logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Console handler
_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_ch.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_ch)

# In-memory buffer to capture logs per run
_buffer: io.StringIO | None = None
_buffer_handler: logging.StreamHandler | None = None


def start_capture() -> None:
    """Start capturing log output into a buffer."""
    global _buffer, _buffer_handler
    _buffer = io.StringIO()
    _buffer_handler = logging.StreamHandler(_buffer)
    _buffer_handler.setLevel(logging.INFO)
    _buffer_handler.setFormatter(_formatter)
    logger.addHandler(_buffer_handler)


def stop_capture() -> str:
    """Stop capturing and return the collected log text."""
    global _buffer, _buffer_handler
    if _buffer_handler:
        logger.removeHandler(_buffer_handler)
    text = _buffer.getvalue() if _buffer else ""
    _buffer = None
    _buffer_handler = None
    return text
