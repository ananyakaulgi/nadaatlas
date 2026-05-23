from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .artist import Artist
    from .artist_instrument import ArtistInstrument
    from .tradition import MusicalTradition


class Instrument(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "instruments"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name_native: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Plain listener-facing family: Stringed, Wind, Brass, Percussion, Keyboard, Electronic
    instrument_family: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hornbostel_sachs: Mapped[str | None] = mapped_column(String(64), nullable=True)
    hs_category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    tradition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("musical_traditions.id", ondelete="SET NULL"),
        nullable=True,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    origin_region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    materials: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    # Relationships
    tradition: Mapped[MusicalTradition | None] = relationship(
        "MusicalTradition", back_populates="instruments", foreign_keys=[tradition_id]
    )
    artist_instruments: Mapped[list[ArtistInstrument]] = relationship(
        "ArtistInstrument", back_populates="instrument"
    )
    primary_for_artists: Mapped[list[Artist]] = relationship(
        "Artist",
        back_populates="primary_instrument",
        foreign_keys="Artist.primary_instrument_id",
    )
