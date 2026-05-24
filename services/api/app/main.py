import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.core.database import init_db
from app.core.logging import configure_logging, get_logger, request_id_var
from app.core.middleware import AuditLogMiddleware, SecurityHeadersMiddleware
from app.core.rate_limiter import limiter
from app.routers import (
    albums,
    artists,
    composers,
    compositions,
    feedback,
    genres,
    health,
    instruments,
    ragas,
    regions,
    talas,
    tracks,
    traditions,
)

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings)
    logger.info("startup", app=settings.APP_NAME, env=settings.APP_ENV)
    await init_db()
    logger.info("database_connected")
    redis = Redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=False)
    app.state.redis = redis
    logger.info("redis_connected")
    yield
    await redis.aclose()
    logger.info("shutdown")


app = FastAPI(
    title="MusiCompass API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Return 409 Conflict for unique-constraint / FK violations instead of 500."""
    return JSONResponse(
        status_code=409,
        content={"error": "Resource already exists or violates a uniqueness constraint"},
    )

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
app.include_router(regions.router)
app.include_router(genres.router)
app.include_router(instruments.router)
app.include_router(artists.router)
app.include_router(albums.router)
app.include_router(tracks.router)
app.include_router(ragas.router)
app.include_router(talas.router)
app.include_router(composers.router)
app.include_router(compositions.router)
app.include_router(feedback.router)

# Auth router — added by the security agent; skip gracefully if not yet present
try:
    from app.routers import auth as auth_router  # type: ignore[import]
    app.include_router(auth_router.router)
except ImportError:
    logger.warning("auth_router_not_found", detail="Security layer not yet installed")


# ---------------------------------------------------------------------------
# Patch OpenAPI schema to add HTTPBearer so Swagger shows a plain token field
# ---------------------------------------------------------------------------
from fastapi.openapi.utils import get_openapi  # noqa: E402


def _custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    # Add BearerAuth as an option on every operation
    for path_item in schema.get("paths", {}).values():
        for operation in path_item.values():
            if isinstance(operation, dict) and "security" in operation:
                operation["security"].append({"BearerAuth": []})
    app.openapi_schema = schema
    return schema


app.openapi = _custom_openapi
