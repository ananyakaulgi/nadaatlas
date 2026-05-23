from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .album import Album
    from .artist import Artist
    from .composer import Composer
    from .composition import Composition
    from .instrument import Instrument
    from .region import Region
    from .track import Track


class MusicalTradition(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "musical_traditions"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name_native: Mapped[str | None] = mapped_column(String(512), nullable=True)
    region_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("regions.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Denormalised label kept for quick display without a JOIN
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    subregion: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    origin_period: Mapped[str | None] = mapped_column(String(255), nullable=True)
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    region_obj: Mapped[Region | None] = relationship(
        "Region", back_populates="traditions", foreign_keys=[region_id]
    )
    artists: Mapped[list[Artist]] = relationship(
        "Artist", back_populates="tradition", foreign_keys="Artist.tradition_id"
    )
    albums: Mapped[list[Album]] = relationship(
        "Album", back_populates="tradition", foreign_keys="Album.tradition_id"
    )
    instruments: Mapped[list[Instrument]] = relationship(
        "Instrument", back_populates="tradition", foreign_keys="Instrument.tradition_id"
    )
    tracks: Mapped[list[Track]] = relationship(
        "Track", back_populates="tradition", foreign_keys="Track.tradition_id"
    )
    composers: Mapped[list[Composer]] = relationship(
        "Composer", back_populates="tradition", foreign_keys="Composer.tradition_id"
    )
    compositions: Mapped[list[Composition]] = relationship(
        "Composition", back_populates="tradition", foreign_keys="Composition.tradition_id"
    )
