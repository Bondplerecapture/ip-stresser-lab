"""StressContract — the interface plugins implement.

Extensions subclass this and are discovered by the registry. The host
only ever calls `prepare`, `run`, and `teardown`, in that order.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StressResult:
    method: str
    target: str
    port: int
    duration: float
    packets_sent: int = 0
    bytes_sent: int = 0
    errors: int = 0
    eps: float = 0.0
    meta: dict[str, Any] = field(default_factory=dict)


class StressContract(ABC):
    """Base class for every ip-stresser-lab extension."""

    #: unique method name, e.g. "syn", "udp", "http"
    method: str = "base"
    #: human description surfaced in `--list`
    description: str = ""
    version: str = "0.0.0"

    @abstractmethod
    async def prepare(self, config: dict[str, Any]) -> None:
        """One-time setup. Raise to abort host startup."""

    @abstractmethod
    async def run(
        self,
        *,
        target: str,
        port: int,
        duration: int,
        concurrency: int,
    ) -> StressResult:
        """Run the attack loop. Must return within `duration` seconds + teardown."""

    async def teardown(self) -> None:
        """Optional cleanup. Default no-op."""
        return None