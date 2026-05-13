"""Logging setup for the scraper module."""

import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "scraper.log"

logger = logging.getLogger("scraper")
logger.setLevel(logging.INFO)

# File handler – append, UTF-8
_fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
_fh.setLevel(logging.INFO)
_fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(_fh)

# Console handler – so prints still appear in CI / terminal
_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
_ch.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(_ch)
