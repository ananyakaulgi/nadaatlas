"""
Resilient async HTTP client with rate limiting, retry, and structured logging.
"""
from __future__ import annotations

import asyncio
import time
from types import TracebackType
from typing import Any

import httpx
import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from config import settings

logger = structlog.get_logger(__name__)

_USER_AGENT = (
    f"NādaAtlas/{settings.worker_version} (contact: {settings.musicbrainz_contact})"
)


class ResilientHttpClient:
    """
    Async HTTP client wrapping httpx.AsyncClient with:
      - per-instance rate limiting via asyncio.Semaphore + token-bucket pacing
      - exponential back-off retry on transient HTTP errors
      - structured logging on every request
    """

    def __init__(
        self,
        base_url: str = "",
        rate_limit_per_second: float = 1.0,
        timeout: float = 30.0,
    ) -> None:
        self._base_url = base_url
        self._rate_limit_per_second = rate_limit_per_second
        self._min_interval = 1.0 / rate_limit_per_second
        self._timeout = timeout
        self._semaphore = asyncio.Semaphore(1)
        self._last_request_time: float = 0.0
        self._client: httpx.AsyncClient | None = None

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    async def __aenter__(self) -> "ResilientHttpClient":
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=self._timeout,
            headers={"User-Agent": _USER_AGENT},
            follow_redirects=True,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    # ── Rate limiting ─────────────────────────────────────────────────────────

    async def _throttle(self) -> None:
        """Enforce minimum inter-request interval."""
        async with self._semaphore:
            now = time.monotonic()
            elapsed = now - self._last_request_time
            wait = self._min_interval - elapsed
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_request_time = time.monotonic()

    # ── Internal request dispatch ─────────────────────────────────────────────

    async def _request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if self._client is None:
            raise RuntimeError(
                "ResilientHttpClient must be used as an async context manager."
            )
        await self._throttle()
        start = time.monotonic()
        response = await self._client.request(
            method,
            url,
            params=params,
            json=json,
            headers=headers,
        )
        elapsed_ms = round((time.monotonic() - start) * 1000, 1)
        logger.info(
            "http_request",
            method=method,
            url=str(response.url),
            status=response.status_code,
            elapsed_ms=elapsed_ms,
        )
        response.raise_for_status()
        return response.json()

    # ── Public API ────────────────────────────────────────────────────────────

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    async def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET request with automatic retry on transient HTTP errors."""
        return await self._request("GET", url, params=params, headers=headers)

    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        wait=wait_exponential(multiplier=1, min=1, max=60),
        stop=stop_after_attempt(5),
        reraise=True,
    )
    async def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """POST request with automatic retry on transient HTTP errors."""
        return await self._request("POST", url, json=json, headers=headers)
