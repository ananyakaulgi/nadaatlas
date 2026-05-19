from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from app.core.config import get_settings

settings = get_settings()

_engine = None
_async_session_local = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            settings.DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=settings.DEBUG,
        )
    return _engine


def _get_session_factory():
    global _async_session_local
    if _async_session_local is None:
        _async_session_local = async_sessionmaker(
            _get_engine(),
            expire_on_commit=False,
            class_=AsyncSession,
        )
    return _async_session_local


# Module-level convenience alias; resolves lazily on first use
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    return _get_session_factory()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields an async DB session."""
    factory = _get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Called at application startup to verify DB connectivity.

    Table creation is managed by Alembic migrations, not here.
    """
    engine = _get_engine()
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
