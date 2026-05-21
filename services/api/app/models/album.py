from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .artist import Artist
    from .track import Track
    from .tradition import MusicalTradition


class Album(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "albums"

    title: Mapped[str] = mapped_column(String(512), nullable=False)
    title_native: Mapped[str | None] = mapped_column(String(512), nullable=True)
    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        nullable=False,
    )
    musicbrainz_id: Mapped[str | None] = mapped_column(
        String(36), unique=True, nullable=True
    )
    release_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    album_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    tradition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("musical_traditions.id", ondelete="SET NULL"),
        nullable=True,
    )
    musical_tradition: Mapped[str | None] = mapped_column(String(255), nullable=True)
    label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cover_image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    spotify_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    artist: Mapped[Artist] = relationship(
        "Artist", back_populates="albums", foreign_keys=[artist_id]
    )
    tradition: Mapped[MusicalTradition | None] = relationship(
        "MusicalTradition", back_populates="albums", foreign_keys=[tradition_id]
    )
    tracks: Mapped[list[Track]] = relationship(
        "Track", back_populates="album", foreign_keys="Track.album_id"
    )
