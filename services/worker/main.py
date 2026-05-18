"""
NādaAtlas worker service entry point.

Configures APScheduler with:
  - AsyncSQLAlchemyJobStore for durable job persistence
  - One scheduled job per data source (no overlapping runs enforced)
  - Graceful shutdown on SIGTERM / SIGINT
  - Structured logging for all lifecycle events
"""
from __future__ import annotations

import asyncio
import logging
import signal
import sys
from typing import Any

import structlog
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings
from jobs.musicbrainz import MusicBrainzIngestionJob
from jobs.spotify import SpotifyIngestionJob
from jobs.wikidata import WikidataIngestionJob
from jobs.wikipedia import WikipediaIngestionJob

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        getattr(logging, settings.log_level.upper(), logging.INFO)
    ),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

log = structlog.get_logger("main")

# ---------------------------------------------------------------------------
# DB engine (sync DSN for APScheduler job store; async DSN for application)
# ---------------------------------------------------------------------------

# APScheduler's SQLAlchemyJobStore requires a *synchronous* SQLAlchemy URL.
# We derive it by replacing the asyncpg driver prefix.
_SYNC_DB_URL = settings.database_url.replace(
    "postgresql+asyncpg://", "postgresql://"
).replace("asyncpg://", "postgresql://")

_async_engine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
_session_factory: async_sessionmaker = async_sessionmaker(
    _async_engine, expire_on_commit=False
)

# ---------------------------------------------------------------------------
# Job factory helpers
# ---------------------------------------------------------------------------


def _make_musicbrainz_job() -> MusicBrainzIngestionJob:
    return MusicBrainzIngestionJob(_session_factory, settings)


def _make_wikipedia_job() -> WikipediaIngestionJob:
    return WikipediaIngestionJob(_session_factory, settings)


def _make_wikidata_job() -> WikidataIngestionJob:
    return WikidataIngestionJob(_session_factory, settings)


def _make_spotify_job() -> SpotifyIngestionJob:
    return SpotifyIngestionJob(_session_factory, settings)


# ---------------------------------------------------------------------------
# Scheduled job wrappers
# (APScheduler calls plain functions; we create a fresh job instance each run
#  so there is no shared mutable state between executions.)
# ---------------------------------------------------------------------------


async def _run_musicbrainz_full() -> None:
    log.info("scheduled_job_start", job="musicbrainz_full")
    await _make_musicbrainz_job().run()
    log.info("scheduled_job_done", job="musicbrainz_full")


async def _run_musicbrainz_delta() -> None:
    """
    Delta run: only newly-tagged artists (last 6 hours window).
    For now delegates to the same full job; a future optimisation can pass
    a `since` timestamp to limit the search scope.
    """
    log.info("scheduled_job_start", job="musicbrainz_delta")
    await _make_musicbrainz_job().run()
    log.info("scheduled_job_done", job="musicbrainz_delta")


async def _run_wikipedia_enrich() -> None:
    log.info("scheduled_job_start", job="wikipedia_enrich")
    await _make_wikipedia_job().run()
    log.info("scheduled_job_done", job="wikipedia_enrich")


async def _run_wikidata_sync() -> None:
    log.info("scheduled_job_start", job="wikidata_sync")
    await _make_wikidata_job().run()
    log.info("scheduled_job_done", job="wikidata_sync")


async def _run_spotify_enrich() -> None:
    log.info("scheduled_job_start", job="spotify_enrich")
    await _make_spotify_job().run()
    log.info("scheduled_job_done", job="spotify_enrich")


# ---------------------------------------------------------------------------
# Scheduler setup
# ---------------------------------------------------------------------------

_JOB_DEFAULTS: dict[str, Any] = {
    "coalesce": True,   # collapse missed firings into one
    "max_instances": 1, # never run the same job concurrently
}

_JOBSTORES: dict[str, Any] = {
    "default": SQLAlchemyJobStore(url=_SYNC_DB_URL, tablename="apscheduler_jobs"),
}

_EXECUTORS: dict[str, Any] = {
    "default": AsyncIOExecutor(),
}


def _build_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(
        jobstores=_JOBSTORES,
        executors=_EXECUTORS,
        job_defaults=_JOB_DEFAULTS,
        timezone="UTC",
    )

    # ── MusicBrainz full ingestion — daily 02:00 UTC ───────────────────────
    scheduler.add_job(
        _run_musicbrainz_full,
        trigger="cron",
        hour=2,
        minute=0,
        id="musicbrainz_full",
        name="MusicBrainz full ingestion",
        replace_existing=True,
    )

    # ── MusicBrainz delta — every 6 hours ─────────────────────────────────
    scheduler.add_job(
        _run_musicbrainz_delta,
        trigger="interval",
        hours=6,
        id="musicbrainz_delta",
        name="MusicBrainz delta ingestion",
        replace_existing=True,
    )

    # ── Wikipedia enrichment — every 12 hours ─────────────────────────────
    scheduler.add_job(
        _run_wikipedia_enrich,
        trigger="interval",
        hours=12,
        id="wikipedia_enrich",
        name="Wikipedia biography enrichment",
        replace_existing=True,
    )

    # ── Wikidata sync — daily 04:00 UTC ───────────────────────────────────
    scheduler.add_job(
        _run_wikidata_sync,
        trigger="cron",
        hour=4,
        minute=0,
        id="wikidata_sync",
        name="Wikidata entity sync",
        replace_existing=True,
    )

    # ── Spotify enrichment — every 24 hours ───────────────────────────────
    scheduler.add_job(
        _run_spotify_enrich,
        trigger="interval",
        hours=24,
        id="spotify_enrich",
        name="Spotify artist enrichment",
        replace_existing=True,
    )

    return scheduler


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> None:
    log.info(
        "worker_starting",
        version=settings.worker_version,
        log_level=settings.log_level,
    )

    scheduler = _build_scheduler()

    # Graceful shutdown
    stop_event = asyncio.Event()

    def _handle_signal(sig: signal.Signals) -> None:
        log.info("signal_received", signal=sig.name)
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, _handle_signal, sig)

    scheduler.start()

    # Log all registered jobs on startup
    for job in scheduler.get_jobs():
        next_run = job.next_run_time.isoformat() if job.next_run_time else "N/A"
        log.info(
            "job_registered",
            job_id=job.id,
            job_name=job.name,
            next_run=next_run,
        )

    log.info("worker_ready", message="Scheduler running; waiting for signal to stop.")

    await stop_event.wait()

    log.info("worker_shutting_down")
    scheduler.shutdown(wait=True)
    await _async_engine.dispose()
    log.info("worker_stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
