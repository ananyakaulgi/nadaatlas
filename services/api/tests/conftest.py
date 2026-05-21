"""
Shared pytest fixtures for the MusiCompass API test suite.

Test database strategy
----------------------
We use a real PostgreSQL database (`nadaatlas_test`) so that PostgreSQL-specific
column types (UUID, ARRAY, pgvector Vector) are supported natively.  The
`nadaatlas_test` database is created automatically via the `test_db_engine`
session-scoped fixture if it does not yet exist.

The `pgvector` extension is registered on the test database so SQLAlchemy can
map `Vector(1536)` columns without crashing.  The Artist.embedding column is
nullable, so tests can omit it without issue.

Dependency overrides
---------------------
`app.dependency_overrides` is used to inject the in-transaction test session for
every request so each test operates on an isolated, rolled-back transaction.
Redis is replaced with `fakeredis` so no live Redis instance is required.

How sessions work
------------------
A single `AsyncConnection` is held open for the duration of each test.  A
`AsyncSession` is bound to a nested transaction (SAVEPOINT) so that the outer
transaction can be rolled back after the test, restoring DB state.  The app
receives a session bound to the same connection so it writes to the same DB
state the test assertions can see.
"""
from __future__ import annotations

import asyncio
import os

# ---------------------------------------------------------------------------
# Ensure tests can import `app` regardless of working directory
# ---------------------------------------------------------------------------
import sys
from collections.abc import AsyncGenerator

import asyncpg
import pytest
import pytest_asyncio
from fakeredis.aioredis import FakeRedis
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

_API_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _API_ROOT not in sys.path:
    sys.path.insert(0, _API_ROOT)

# ---------------------------------------------------------------------------
# Test database URL — swap database name to nadaatlas_test
# ---------------------------------------------------------------------------
# Allow DATABASE_URL to be overridden by environment (e.g. in Docker the host
# is "postgres", in CI it's "localhost" via service containers).
_PG_HOST = os.environ.get("POSTGRES_HOST", "localhost")
_PG_DSN = f"nadaatlas:75b1675d8970658acea1d887c13203c1@{_PG_HOST}:5432"

TEST_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    f"postgresql+asyncpg://{_PG_DSN}/nadaatlas_test",
)

# The admin URL is used solely to CREATE the test database when missing.
ADMIN_DATABASE_URL = os.environ.get(
    "ADMIN_DATABASE_URL",
    f"postgresql+asyncpg://{_PG_DSN}/nadaatlas",
)

# Override the DATABASE_URL env var before any app code reads it so that
# `get_settings()` (which is cached via lru_cache) sees the test value.
os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci-do-not-use-in-production")

# ---------------------------------------------------------------------------
# App imports — must come AFTER env vars are set so Settings resolves correctly
# ---------------------------------------------------------------------------
from app.core.auth import get_redis  # noqa: E402
from app.core.database import get_db  # noqa: E402
from app.core.security import hash_password  # noqa: E402
from app.main import app  # noqa: E402
from app.models.album import Album  # noqa: E402
from app.models.artist import Artist  # noqa: E402
from app.models.base import Base  # noqa: E402
from app.models.instrument import Instrument  # noqa: E402
from app.models.tradition import MusicalTradition  # noqa: E402
from app.models.user import User  # noqa: E402

# ---------------------------------------------------------------------------
# Session-scoped: ensure test database exists + schema is ready
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def event_loop():
    """Single event loop for the entire test session (pytest-asyncio requirement)."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_engine():
    """
    Session-scoped engine.

    1. Connects to the default `nadaatlas` DB and creates `nadaatlas_test` if absent.
    2. Registers the `pgvector` extension so Vector columns map correctly.
    3. Runs `create_all` to build the schema from SQLAlchemy metadata.
    4. Yields the engine for the session.
    5. Drops all tables at teardown so the next run starts clean.
    """
    # ── Step 1: create test DB if missing ────────────────────────────────────
    try:
        conn = await asyncpg.connect(
            f"postgresql://nadaatlas:75b1675d8970658acea1d887c13203c1"
            f"@{_PG_HOST}:5432/nadaatlas"
        )
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", "nadaatlas_test"
        )
        if not exists:
            # CREATE DATABASE cannot run inside a transaction
            await conn.execute("CREATE DATABASE nadaatlas_test")
        await conn.close()
    except Exception as exc:
        pytest.skip(f"Cannot reach PostgreSQL to create test DB: {exc}")

    # ── Step 2: create engine pointing at nadaatlas_test ─────────────────────
    # NullPool disables connection pooling so every checkout creates a fresh
    # asyncpg connection.  This avoids "Future attached to a different loop"
    # errors that occur when pooled connections created in the session-scoped
    # fixture are later reused inside function-scoped coroutine tasks.
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    # ── Step 3: register pgvector extension + create schema ──────────────────
    async with engine.begin() as conn:
        await conn.execute(
            __import__("sqlalchemy").text("CREATE EXTENSION IF NOT EXISTS vector")
        )
        # Import all models so metadata is populated
        import app.models.album  # noqa: F401
        import app.models.artist  # noqa: F401
        import app.models.artist_instrument  # noqa: F401
        import app.models.instrument  # noqa: F401
        import app.models.tag  # noqa: F401
        import app.models.track  # noqa: F401
        import app.models.tradition  # noqa: F401
        import app.models.user  # noqa: F401

        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    yield engine

    # ── Teardown: drop all tables ─────────────────────────────────────────────
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# ---------------------------------------------------------------------------
# Function-scoped: one rolled-back transaction per test
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def db_connection(test_db_engine) -> AsyncGenerator[AsyncConnection, None]:
    """Open one connection with an outer transaction that rolls back after each test."""
    async with test_db_engine.connect() as conn:
        await conn.begin()
        yield conn
        await conn.rollback()


@pytest_asyncio.fixture()
async def db_session(db_connection: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an AsyncSession bound to the test connection's open transaction.

    Using `join_transaction_mode="create_savepoint"` means the session works
    with SAVEPOINTs so the outer transaction can still be rolled back cleanly.
    """
    session_factory = async_sessionmaker(
        bind=db_connection,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    async with session_factory() as session:
        yield session


# ---------------------------------------------------------------------------
# Redis
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def fake_redis() -> AsyncGenerator[FakeRedis, None]:
    """An in-process fake Redis that resets between tests."""
    redis = FakeRedis()
    yield redis
    await redis.aclose()


# ---------------------------------------------------------------------------
# FastAPI test app with overridden dependencies
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def test_app(db_session: AsyncSession, fake_redis: FakeRedis):
    """Return the FastAPI app with DB + Redis dependencies overridden for tests."""

    async def _override_get_db():
        yield db_session

    async def _override_get_redis():
        return fake_redis

    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_redis] = _override_get_redis

    yield app

    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient wired to the ASGI test app — no network required."""
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://testserver",
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Test user fixtures
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def test_user(db_session: AsyncSession) -> User:
    """Create and persist a regular (non-superuser) test user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPass123!"),
        is_active=True,
        is_superuser=False,
        email_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture()
async def superuser(db_session: AsyncSession) -> User:
    """Create and persist a superuser."""
    user = User(
        email="superuser@example.com",
        hashed_password=hash_password("SuperPass123!"),
        is_active=True,
        is_superuser=True,
        email_verified=True,
    )
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


# ---------------------------------------------------------------------------
# Auth header fixtures — create JWTs directly to avoid rate-limit exhaustion
# ---------------------------------------------------------------------------
# We do NOT call the login endpoint here; that would trigger the per-IP rate
# limiter (10/minute) and fail any test suite with more than 10 authed tests.
# The login endpoint itself is tested in tests/api/test_auth.py.

@pytest_asyncio.fixture()
async def auth_headers(test_user: User) -> dict[str, str]:
    """Return Authorization Bearer headers for `test_user` (token minted directly)."""
    from app.core.security import create_access_token
    token = create_access_token(str(test_user.id))
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture()
async def superuser_headers(superuser: User) -> dict[str, str]:
    """Return Authorization Bearer headers for `superuser` (token minted directly)."""
    from app.core.security import create_access_token
    token = create_access_token(str(superuser.id))
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Domain fixtures
# ---------------------------------------------------------------------------

@pytest_asyncio.fixture()
async def sample_tradition(db_session: AsyncSession) -> MusicalTradition:
    """A persisted MusicalTradition for use in other fixtures / tests."""
    tradition = MusicalTradition(
        name="Hindustani Classical",
        region="South Asia",
        subregion="North India",
        description="Classical music tradition of northern India.",
        is_active=True,
    )
    db_session.add(tradition)
    await db_session.flush()
    await db_session.refresh(tradition)
    return tradition


@pytest_asyncio.fixture()
async def sample_instrument(
    db_session: AsyncSession, sample_tradition: MusicalTradition
) -> Instrument:
    """A persisted Instrument linked to `sample_tradition`."""
    instrument = Instrument(
        name="Sitar",
        name_native="सितार",
        hornbostel_sachs="321.321",
        hs_category="chordophone",
        tradition_id=sample_tradition.id,
        origin_region="South Asia",
        description="A plucked string instrument used in Hindustani music.",
    )
    db_session.add(instrument)
    await db_session.flush()
    await db_session.refresh(instrument)
    return instrument


@pytest_asyncio.fixture()
async def sample_artist(
    db_session: AsyncSession,
    sample_tradition: MusicalTradition,
    sample_instrument: Instrument,
) -> Artist:
    """A persisted Artist linked to `sample_tradition` and `sample_instrument`."""
    artist = Artist(
        name="Ravi Shankar",
        name_native="रवि शंकर",
        musical_tradition="Hindustani Classical",
        tradition_id=sample_tradition.id,
        primary_instrument_id=sample_instrument.id,
        nationality="Indian",
        biography_short="Legendary sitarist and composer.",
    )
    db_session.add(artist)
    await db_session.flush()
    await db_session.refresh(artist)
    return artist


@pytest_asyncio.fixture()
async def sample_album(
    db_session: AsyncSession,
    sample_artist: Artist,
    sample_tradition: MusicalTradition,
) -> Album:
    """A persisted Album linked to `sample_artist`."""
    from datetime import date

    album = Album(
        title="The Living Room Sessions Part 1",
        artist_id=sample_artist.id,
        tradition_id=sample_tradition.id,
        musical_tradition="Hindustani Classical",
        album_type="album",
        release_date=date(2011, 9, 27),
        label="East Meets West",
    )
    db_session.add(album)
    await db_session.flush()
    await db_session.refresh(album)
    return album
