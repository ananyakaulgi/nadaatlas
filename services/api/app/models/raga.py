from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .composition import Composition
    from .track import Track


class Raga(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    A raga is a melodic framework — not a scale, not a song.
    It defines the ascent (arohana), descent (avarohana), characteristic
    phrases (pakad), emotional colour (rasa), and the appropriate time/season
    for performance. The same underlying mode may exist in both Hindustani
    and Carnatic traditions under different names (e.g. Yaman = Kalyani).
    """

    __tablename__ = "ragas"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name_native: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # "hindustani", "carnatic", or "both"
    tradition: Mapped[str] = mapped_column(String(64), nullable=False)

    # For cross-tradition ragas where tradition = "both"
    hindustani_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    carnatic_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Hindustani: parent That in Bhatkhande's 10-That system
    that: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Carnatic: parent Melakarta number (1–72)
    melakarta_number: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Scale structure
    arohana: Mapped[str | None] = mapped_column(String(512), nullable=True)
    avarohana: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Important notes
    vadi: Mapped[str | None] = mapped_column(String(64), nullable=True)
    samvadi: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Characteristic catch-phrase / signature motif
    pakad: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Performance context
    time_of_day: Mapped[str | None] = mapped_column(String(64), nullable=True)
    season: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Emotional quality e.g. "Shringara (love)", "Karuna (pathos)"
    rasa: Mapped[str | None] = mapped_column(String(255), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Relationships
    tracks: Mapped[list[Track]] = relationship(
        "Track", back_populates="raga_obj", foreign_keys="Track.raga_id"
    )
    compositions: Mapped[list[Composition]] = relationship(
        "Composition", back_populates="raga_obj", foreign_keys="Composition.raga_id"
    )

    def __repr__(self) -> str:
        return f"<Raga id={self.id} name={self.name!r} tradition={self.tradition!r}>"
