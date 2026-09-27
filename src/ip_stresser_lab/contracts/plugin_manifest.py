"""Typed view over a plugin's manifest.yaml — validated before load."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PluginManifest:
    method: str
    entry: str
    version: str
    description: str
    author: str
    min_host_version: str = "0.5.0"

    @classmethod
    def from_mapping(cls, raw: dict, *, base: Path) -> "PluginManifest":
        missing = [k for k in ("method", "entry") if k not in raw]
        if missing:
            raise ValueError(f"manifest missing keys: {missing}")
        return cls(
            method=raw["method"],
            entry=raw["entry"],
            version=str(raw.get("version", "0.0.0")),
            description=str(raw.get("description", "")),
            author=str(raw.get("author", "unknown")),
            min_host_version=str(raw.get("min_host_version", "0.5.0")),
        )