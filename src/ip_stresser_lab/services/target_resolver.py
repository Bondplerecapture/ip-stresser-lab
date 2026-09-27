"""Resolve hostnames to A records and cache them for the run duration."""
from __future__ import annotations

import ipaddress
import socket
import time
from dataclasses import dataclass


@dataclass(slots=True)
class ResolvedTarget:
    hostname: str
    ip: str
    resolved_at: float


class TargetResolver:
    def __init__(self, ttl: float = 30.0) -> None:
        self._ttl = ttl
        self._cache: dict[str, ResolvedTarget] = {}

    def resolve(self, host: str) -> str:
        # literal IP short-circuit
        try:
            ipaddress.ip_address(host)
            return host
        except ValueError:
            pass
        now = time.monotonic()
        hit = self._cache.get(host)
        if hit and now - hit.resolved_at < self._ttl:
            return hit.ip
        ip = socket.gethostbyname(host)
        self._cache[host] = ResolvedTarget(hostname=host, ip=ip, resolved_at=now)
        return ip