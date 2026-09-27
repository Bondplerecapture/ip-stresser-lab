"""Merge YAML defaults, env overrides, and CLI-supplied paths."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def load_config(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    # env override: IP_STRESSER__PATHS__LOGS=/var/log/isl
    for key, value in os.environ.items():
        if not key.startswith("IP_STRESSER__"):
            continue
        parts = [p.lower() for p in key.removeprefix("IP_STRESSER__").split("__")]
        node = data
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = value
    return data