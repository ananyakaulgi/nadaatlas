from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .artist import Artist
    from .instrument import Instrument


class ArtistInstrument(Base):
    __tablename__ = "artist_instruments"

    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    instrument_id: Mapped[UUID] = mapped_column(
        ForeignKey("instruments.id", ondelete="CASCADE"),
        primary_key=True,
    )
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    proficiency: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    artist: Mapped[Artist] = relationship(
        "Artist", back_populates="artist_instruments"
    )
    instrument: Mapped[Instrument] = relationship(
        "Instrument", back_populates="artist_instruments"
    )
