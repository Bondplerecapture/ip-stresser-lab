"""Worker pool + rate scheduler used by extensions.

Extensions that just want "N workers hammering for D seconds" should call
`run_workers` instead of rolling their own loop. Keeps rate limiting and
cancellation consistent across plugins.
"""
from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from ip_stresser_lab.contracts.stress_contract import StressResult


@dataclass(slots=True)
class WorkerStats:
    packets_sent: int = 0
    bytes_sent: int = 0
    errors: int = 0


async def run_workers(
    *,
    method: str,
    target: str,
    port: int,
    duration: int,
    concurrency: int,
    worker: Callable[[str, int], Awaitable[tuple[int, int]]],
    pps_cap: int | None = None,
) -> StressResult:
    stats = WorkerStats()
    started = time.monotonic()
    deadline = started + duration
    per_worker_sleep = 0.0 if not pps_cap else concurrency / pps_cap

    async def _loop() -> None:
        while time.monotonic() < deadline:
            try:
                sent, nbytes = await worker(target, port)
                stats.packets_sent += sent
                stats.bytes_sent += nbytes
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001 — a dead socket shouldn't kill the worker
                stats.errors += 1
            if per_worker_sleep:
                await asyncio.sleep(per_worker_sleep)

    tasks = [asyncio.create_task(_loop()) for _ in range(concurrency)]
    try:
        await asyncio.gather(*tasks)
    finally:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    elapsed = max(time.monotonic() - started, 1e-6)
    return StressResult(
        method=method,
        target=target,
        port=port,
        duration=elapsed,
        packets_sent=stats.packets_sent,
        bytes_sent=stats.bytes_sent,
        errors=stats.errors,
        eps=stats.packets_sent / elapsed,
    )