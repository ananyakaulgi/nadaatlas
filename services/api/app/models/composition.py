from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .album import Album
    from .artist import Artist
    from .composer import Composer
    from .raga import Raga
    from .tala import Tala
    from .track import Track
    from .tradition import MusicalTradition


class Composition(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    The abstract musical work — the idea on paper, independent of who performs it.
    One Composition can have many Tracks (recordings).

    Distinct from a Track which is a specific captured performance.
    Example: "Vaatapi Ganapathim Bhaje" is a composition;
    M.S. Subbulakshmi's 1954 recording of it is a track.
    """

    __tablename__ = "compositions"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    title_native: Mapped[str | None] = mapped_column(String(512), nullable=True)

    composer_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("composers.id", ondelete="SET NULL"),
        nullable=True,
    )
    tradition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("musical_traditions.id", ondelete="SET NULL"),
        nullable=True,
    )

    # e.g. "kriti", "bandish", "thumri", "ghazal", "qawwali", "symphony", "sonata", "film"
    composition_type: Mapped[str | None] = mapped_column(String(64), nullable=True)

    raga_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ragas.id", ondelete="SET NULL"),
        nullable=True,
    )
    tala_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("talas.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Free text for Arabic/Turkish traditions — no maqamat table yet
    maqam: Mapped[str | None] = mapped_column(String(255), nullable=True)

    language: Mapped[str | None] = mapped_column(String(64), nullable=True)
    lyrics: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    year_composed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536), nullable=True
    )

    # Relationships
    composer: Mapped[Composer | None] = relationship(
        "Composer", back_populates="compositions", foreign_keys=[composer_id]
    )
    tradition: Mapped[MusicalTradition | None] = relationship(
        "MusicalTradition", back_populates="compositions", foreign_keys=[tradition_id]
    )
    raga_obj: Mapped[Raga | None] = relationship(
        "Raga", back_populates="compositions", foreign_keys=[raga_id]
    )
    tala_obj: Mapped[Tala | None] = relationship(
        "Tala", back_populates="compositions", foreign_keys=[tala_id]
    )
    performances: Mapped[list[CompositionPerformance]] = relationship(
        "CompositionPerformance", back_populates="composition"
    )

    def __repr__(self) -> str:
        return f"<Composition id={self.id} title={self.title!r}>"


class CompositionPerformance(Base):
    """
    Junction table linking a specific Track (recording) to the abstract
    Composition, the performing Artist, and the Album it appears on.
    Composite PK: (composition_id, artist_id, album_id).
    """

    __tablename__ = "composition_performances"

    composition_id: Mapped[UUID] = mapped_column(
        ForeignKey("compositions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    album_id: Mapped[UUID] = mapped_column(
        ForeignKey("albums.id", ondelete="CASCADE"),
        primary_key=True,
    )
    track_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("tracks.id", ondelete="SET NULL"),
        nullable=True,
    )
    performance_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    from datetime import datetime
    from sqlalchemy import DateTime, func
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    composition: Mapped[Composition] = relationship(
        "Composition", back_populates="performances"
    )
    artist: Mapped[Artist] = relationship("Artist")
    album: Mapped[Album] = relationship("Album")
    track: Mapped[Track | None] = relationship("Track")
