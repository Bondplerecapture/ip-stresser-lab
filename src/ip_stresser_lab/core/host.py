"""PluginHost — owns the event loop, the registry, and the dispatch path."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from ip_stresser_lab.contracts.stress_contract import StressContract, StressResult
from ip_stresser_lab.core.registry import ExtensionRegistry

log = logging.getLogger(__name__)


class PluginHost:
    def __init__(self, *, registry: ExtensionRegistry, config: dict[str, Any]) -> None:
        self._registry = registry
        self._config = config
        self._started = False
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        async with self._lock:
            if self._started:
                return
            for meta in self._registry.catalogue().values():
                ext = self._registry.resolve(meta.method)
                if ext is None:
                    continue
                try:
                    await ext.prepare(self._config)
                except Exception as exc:  # noqa: BLE001 — a bad plugin must not kill the host
                    log.error("plugin %s failed prepare: %s", meta.method, exc)
            self._started = True
            log.info("host started with %d extensions", len(self._registry.catalogue()))

    async def dispatch(
        self,
        ext: StressContract,
        *,
        target: str,
        port: int,
        duration: int,
        concurrency: int,
    ) -> StressResult:
        if not self._started:
            raise RuntimeError("host not started")
        log.info("dispatch method=%s target=%s:%d dur=%ds workers=%d",
                 ext.method, target, port, duration, concurrency)
        result = await ext.run(
            target=target, port=port, duration=duration, concurrency=concurrency
        )
        await ext.teardown()
        return result

    async def stop(self) -> None:
        async with self._lock:
            if not self._started:
                return
            for ext in self._registry.iter_loaded():
                try:
                    await ext.teardown()
                except Exception:  # noqa: BLE001
                    log.exception("teardown error for %s", ext.method)
            self._started = False
            log.info("host stopped")