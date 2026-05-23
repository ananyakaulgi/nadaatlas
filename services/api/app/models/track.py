from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer, String, Text  # noqa: F401
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .album import Album
    from .artist import Artist
    from .raga import Raga
    from .tala import Tala
    from .tradition import MusicalTradition


class Track(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "tracks"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    title_native: Mapped[str | None] = mapped_column(String(512), nullable=True)
    album_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("albums.id", ondelete="SET NULL"),
        nullable=True,
    )
    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        nullable=False,
    )
    musicbrainz_id: Mapped[str | None] = mapped_column(
        String(36), unique=True, nullable=True
    )
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    track_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    musical_tradition: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tradition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("musical_traditions.id", ondelete="SET NULL"),
        nullable=True,
    )
    raga_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ragas.id", ondelete="SET NULL"),
        nullable=True,
    )
    tala_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("talas.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Free-text fallback — kept until ragas/talas tables are seeded and backfilled
    raga: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tala: Mapped[str | None] = mapped_column(String(255), nullable=True)
    maqam: Mapped[str | None] = mapped_column(String(255), nullable=True)
    lyrics: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536), nullable=True
    )
    youtube_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    spotify_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    # Relationships
    album: Mapped[Album | None] = relationship(
        "Album", back_populates="tracks", foreign_keys=[album_id]
    )
    artist: Mapped[Artist] = relationship(
        "Artist", back_populates="tracks", foreign_keys=[artist_id]
    )
    tradition: Mapped[MusicalTradition | None] = relationship(
        "MusicalTradition", back_populates="tracks", foreign_keys=[tradition_id]
    )
    raga_obj: Mapped[Raga | None] = relationship(
        "Raga", back_populates="tracks", foreign_keys=[raga_id]
    )
    tala_obj: Mapped[Tala | None] = relationship(
        "Tala", back_populates="tracks", foreign_keys=[tala_id]
    )
