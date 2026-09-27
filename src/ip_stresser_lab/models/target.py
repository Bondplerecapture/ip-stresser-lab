"""Target — validated representation of an attack destination."""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Target:
    host: str
    port: int
    resolved_ip: str | None = None

    def __post_init__(self) -> None:
        if not (0 < self.port < 65536):
            raise ValueError(f"port out of range: {self.port}")
        if self.resolved_ip:
            ipaddress.ip_address(self.resolved_ip)

    @property
    def is_literal(self) -> bool:
        try:
            ipaddress.ip_address(self.host)
            return True
        except ValueError:
            return False

    def label(self) -> str:
        return f"{self.resolved_ip or self.host}:{self.port}"