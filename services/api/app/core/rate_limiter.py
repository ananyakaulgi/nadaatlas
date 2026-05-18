"""Rate limiter configuration using slowapi.

Default limits:
  - Unauthenticated: 60 requests / minute (applied globally)
  - Authenticated:   300 requests / minute (opt-in via authenticated_rate_limit)

Wire up to the FastAPI app in main.py:

    from slowapi.errors import RateLimitExceeded
    from slowapi import _rate_limit_exceeded_handler
    from app.core.rate_limiter import limiter

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
"""
from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

# Global limiter — key on client IP, default 60/minute for unauthenticated traffic
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["60/minute"],
    # Headers added to every response so clients can observe their quota
    headers_enabled=True,
)


def rate_limit(limit_string: str):
    """Convenience decorator that wraps ``limiter.limit``.

    Usage::

        @router.get("/endpoint")
        @rate_limit("10/minute")
        async def my_endpoint(request: Request): ...
    """
    return limiter.limit(limit_string)


def authenticated_rate_limit(limit_string: str = "300/minute"):
    """Higher-quota rate limit for authenticated endpoints.

    Usage::

        @router.get("/private")
        @authenticated_rate_limit()
        async def private_endpoint(request: Request): ...
    """
    return limiter.limit(limit_string)
