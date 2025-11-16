# westmarch/core/logging.py
from __future__ import annotations
import datetime

LOGGING_ENABLED = True   # flip to False to silence logs


def log(message: str):
    """Simple timestamped logger."""
    if not LOGGING_ENABLED:
        return

    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")