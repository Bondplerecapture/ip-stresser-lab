"""ExtensionRegistry — discovers plugin packages and hot-loads their entry module.

A plugin lives under `plugins/<name>/` and ships a `manifest.yaml`:

    method: syn
    entry: plugin:SynFloodExtension
    version: 0.3.1

The registry imports the entry module, resolves the class, validates it
subclasses StressContract, instantiates it, and registers it by method.
"""
from __future__ import annotations

import importlib.util
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

import yaml

from ip_stresser_lab.contracts.stress_contract import StressContract
from ip_stresser_lab.utils.errors import PluginLoadError

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PluginMeta:
    method: str
    version: str
    description: str
    path: Path


class ExtensionRegistry:
    def __init__(self, *, plugin_root: Path, config: dict[str, Any]) -> None:
        self._root = plugin_root
        self._config = config
        self._meta: dict[str, PluginMeta] = {}
        self._loaded: dict[str, StressContract] = {}

    def discover(self) -> None:
        if not self._root.exists():
            log.warning("plugin root %s does not exist", self._root)
            return
        for manifest in self._root.glob("*/manifest.yaml"):
            try:
                self._load_manifest(manifest)
            except Exception as exc:  # noqa: BLE001
                log.error("failed to load plugin at %s: %s", manifest.parent.name, exc)

    def _load_manifest(self, manifest: Path) -> None:
        raw = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
        method = raw["method"]
        entry_mod, _, entry_cls = raw["entry"].partition(":")
        pkg_dir = manifest.parent
        mod_name = f"ip_stresser_plugin_{method}_{pkg_dir.name}"

        spec = importlib.util.spec_from_file_location(
            mod_name, pkg_dir / f"{entry_mod}.py"
        )
        if spec is None or spec.loader is None:
            raise PluginLoadError(f"cannot load module {entry_mod} from {pkg_dir}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)

        cls = getattr(module, entry_cls, None)
        if cls is None or not issubclass(cls, StressContract):
            raise PluginLoadError(f"{entry_cls} does not implement StressContract")

        instance: StressContract = cls()
        self._meta[method] = PluginMeta(
            method=method,
            version=str(raw.get("version", instance.version)),
            description=str(raw.get("description", instance.description)),
            path=pkg_dir,
        )
        self._loaded[method] = instance
        log.info("registered extension '%s' v%s", method, self._meta[method].version)

    def resolve(self, method: str) -> StressContract | None:
        return self._loaded.get(method)

    def catalogue(self) -> dict[str, PluginMeta]:
        return dict(self._meta)

    def iter_loaded(self) -> Iterator[StressContract]:
        return iter(self._loaded.values())