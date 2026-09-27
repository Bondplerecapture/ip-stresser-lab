"""Token-bucket rate limiter. Extensions pull one token per packet."""
from __future__ import annotations

import asyncio
import time


class TokenBucket:
    """Async token bucket.

    capacity  : burst size (tokens)
    refill_hz : tokens replenished per second
    """

    def __init__(self, capacity: int, refill_hz: float) -> None:
        self._capacity = float(capacity)
        self._tokens = float(capacity)
        self._refill = refill_hz
        self._ts = time.monotonic()
        self._lock = asyncio.Lock()

    async def take(self) -> None:
        async with self._lock:
            now = time.monotonic()
            self._tokens = min(self._capacity, self._tokens + (now - self._ts) * self._refill)
            self._ts = now
            if self._tokens < 1.0:
                deficit = (1.0 - self._tokens) / self._refill
                await asyncio.sleep(deficit)
                self._tokens = 0.0
            else:
                self._tokens -= 1.0