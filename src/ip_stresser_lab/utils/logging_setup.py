"""Logging setup — Rich handler on TTY, rotating file elsewhere."""
from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

from rich.logging import RichHandler


def configure_logging(*, verbosity: int, log_dir: str | Path) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(level)
    for h in list(root.handlers):
        root.removeHandler(h)

    root.addHandler(RichHandler(rich_tracebacks=True, show_path=False))
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / "ip-stresser-lab.log", maxBytes=8 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-7s %(name)s :: %(message)s"
    ))
    root.addHandler(file_handler)