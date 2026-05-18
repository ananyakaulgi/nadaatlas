import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import configure_logging, get_logger, request_id_var
from app.core.middleware import AuditLogMiddleware, SecurityHeadersMiddleware
from app.core.rate_limiter import limiter
from app.routers import health, traditions, instruments, artists, albums, tracks

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings)
    logger.info("startup", app=settings.APP_NAME, env=settings.APP_ENV)
    await init_db()
    logger.info("database_connected")
    yield
    logger.info("shutdown")


app = FastAPI(
    title="NādaAtlas API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ---------------------------------------------------------------------------
# Sentry (optional — only initialised when DSN is configured)
# ---------------------------------------------------------------------------
if settings.SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.APP_ENV,
        integrations=[StarletteIntegration(), FastApiIntegration()],
        traces_sample_rate=0.1,
    )

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next) -> Response:
    """Attach a UUID request ID to every request and surface it in the response."""
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    token = request_id_var.set(request_id)
    try:
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        request_id_var.reset(token)


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(health.router)
app.include_router(traditions.router)
app.include_router(instruments.router)
app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(tracks.router)

# Auth router — added by the security agent; skip gracefully if not yet present
try:
    from app.routers import auth as auth_router  # type: ignore[import]
    app.include_router(auth_router.router)
except ImportError:
    logger.warning("auth_router_not_found", detail="Security layer not yet installed")
