"""RunState — snapshot of an in-flight stress run, used by the dashboard."""
from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass(slots=True)
class RunState:
    method: str
    target: str
    port: int
    started_at: float = field(default_factory=time.monotonic)
    packets_sent: int = 0
    bytes_sent: int = 0
    errors: int = 0

    @property
    def elapsed(self) -> float:
        return max(time.monotonic() - self.started_at, 1e-6)

    @property
    def eps(self) -> float:
        return self.packets_sent / self.elapsed

    @property
    def mbps(self) -> float:
        return (self.bytes_sent * 8) / self.elapsed / 1_000_000