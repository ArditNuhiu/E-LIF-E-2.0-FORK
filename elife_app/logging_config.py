from __future__ import annotations

import logging
from pathlib import Path


def setup_logging() -> logging.Logger:
    """Configure root logger with terminal and file handlers."""
    Path("logs").mkdir(exist_ok=True)

    fmt = "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if root.handlers:
        return root

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("logs/elife.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root.addHandler(stream_handler)
    root.addHandler(file_handler)

    return root
