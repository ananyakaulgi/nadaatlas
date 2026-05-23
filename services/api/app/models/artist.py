from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .album import Album
    from .artist_instrument import ArtistInstrument
    from .genre import ArtistGenre
    from .instrument import Instrument
    from .tag import ArtistTag
    from .track import Track
    from .tradition import MusicalTradition


class Artist(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "artists"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_native: Mapped[str | None] = mapped_column(String(512), nullable=True)
    name_sort: Mapped[str | None] = mapped_column(String(255), nullable=True)
    musicbrainz_id: Mapped[str | None] = mapped_column(
        String(36), unique=True, nullable=True
    )
    wikidata_id: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True
    )
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)
    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    biography_short: Mapped[str | None] = mapped_column(String(500), nullable=True)
    born: Mapped[date | None] = mapped_column(Date, nullable=True)
    died: Mapped[date | None] = mapped_column(Date, nullable=True)
    birth_place: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(255), nullable=True)
    musical_tradition: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tradition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("musical_traditions.id", ondelete="SET NULL"),
        nullable=True,
    )
    primary_instrument_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("instruments.id", ondelete="SET NULL"),
        nullable=True,
    )
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(1536), nullable=True
    )
    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    spotify_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    youtube_channel_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    tradition: Mapped[MusicalTradition | None] = relationship(
        "MusicalTradition", back_populates="artists", foreign_keys=[tradition_id]
    )
    primary_instrument: Mapped[Instrument | None] = relationship(
        "Instrument",
        back_populates="primary_for_artists",
        foreign_keys=[primary_instrument_id],
    )
    albums: Mapped[list[Album]] = relationship(
        "Album", back_populates="artist", foreign_keys="Album.artist_id"
    )
    tracks: Mapped[list[Track]] = relationship(
        "Track", back_populates="artist", foreign_keys="Track.artist_id"
    )
    artist_instruments: Mapped[list[ArtistInstrument]] = relationship(
        "ArtistInstrument", back_populates="artist"
    )
    artist_tags: Mapped[list[ArtistTag]] = relationship(
        "ArtistTag", back_populates="artist"
    )
    artist_genres: Mapped[list[ArtistGenre]] = relationship(
        "ArtistGenre", back_populates="artist"
    )
