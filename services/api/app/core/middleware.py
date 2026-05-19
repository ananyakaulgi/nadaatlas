"""Security, request ID, and audit-log middleware.

Middleware stack (applied outermost-first in main.py):
  1. SecurityHeadersMiddleware  — defence-in-depth HTTP headers
  2. RequestIDMiddleware        — per-request UUID correlation
  3. AuditLogMiddleware         — structured request/response logging
"""
from __future__ import annotations

import time
import uuid
from contextvars import ContextVar

import structlog
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.core.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

# ContextVar so structlog processors can read the current request ID without
# threading it through every call frame.
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")


# ---------------------------------------------------------------------------
# 1. Security Headers
# ---------------------------------------------------------------------------

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security-relevant HTTP headers to every response.

    HSTS is only set in production to avoid breaking local TLS-less dev flows.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self._is_production = settings.APP_ENV == "production"

    # Swagger/ReDoc load assets from jsdelivr — relax CSP only for those paths
    _DOCS_PATHS = {"/api/docs", "/api/redoc", "/openapi.json"}

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        if request.url.path in self._DOCS_PATHS:
            # Swagger UI fetches JS/CSS from cdn.jsdelivr.net
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
                "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self'; "
                "worker-src blob:"
            )
        else:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self'"
            )

        if self._is_production:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response


# ---------------------------------------------------------------------------
# 2. Request ID
# ---------------------------------------------------------------------------

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Attach a UUID correlation ID to every request and response.

    Uses the incoming ``X-Request-ID`` header if present (for upstream proxy
    passthrough); otherwise generates a fresh UUID v4.

    Also binds the ID into a ``ContextVar`` so structlog picks it up
    automatically via a custom processor.
    """

    _HEADER = "X-Request-ID"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        req_id = request.headers.get(self._HEADER) or str(uuid.uuid4())
        token = request_id_ctx.set(req_id)
        try:
            response = await call_next(request)
        finally:
            request_id_ctx.reset(token)

        response.headers[self._HEADER] = req_id
        return response


# ---------------------------------------------------------------------------
# 3. Audit Log
# ---------------------------------------------------------------------------

_MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Emit a structured log line for every HTTP request.

    Fields logged on every request:
      method, path, status_code, duration_ms, request_id, user_agent

    Additional fields for mutating requests (POST/PUT/PATCH/DELETE):
      user_id — extracted from the Bearer JWT ``sub`` claim if present;
                 absent (not an error) for unauthenticated calls.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        log_fields: dict = {
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "request_id": request_id_ctx.get(""),
            "user_agent": request.headers.get("User-Agent", ""),
        }

        if request.method in _MUTATING_METHODS:
            user_id = _extract_user_id(request)
            if user_id:
                log_fields["user_id"] = user_id

        logger.info("http_request", **log_fields)
        return response


def _extract_user_id(request: Request) -> str | None:
    """Best-effort extraction of ``sub`` from the Authorization Bearer token.

    Returns ``None`` rather than raising — audit logging must never block a
    response, and unauthenticated requests legitimately have no token.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    raw_token = auth_header.removeprefix("Bearer ").strip()
    try:
        # Decode without verification — we only want the ``sub`` for logging.
        # Full verification happens in the auth dependency.
        payload = jwt.get_unverified_claims(raw_token)
        return payload.get("sub")
    except (JWTError, Exception):
        return None
