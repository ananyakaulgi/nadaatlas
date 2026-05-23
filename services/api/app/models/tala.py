from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .composition import Composition
    from .track import Track


class Tala(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    A tala is a rhythmic cycle — a fixed, repeating time-signature that
    governs when a composition begins and how it breathes.

    Hindustani talas use a clap pattern (vibhag with sam/tali/khali marks).
    Carnatic talas combine seven suladi talas with five jatis (groupings)
    to produce 35 standard talas, each with a different beat count.
    """

    __tablename__ = "talas"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name_native: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # "hindustani", "carnatic", or "both"
    tradition: Mapped[str] = mapped_column(String(64), nullable=False)

    # Total beat count (matras / aksharas) e.g. 16 for Teentaal, 8 for Adi
    beats: Mapped[int] = mapped_column(Integer, nullable=False)

    # Hindustani: subdivision pattern e.g. "4+4+4+4" for Teentaal
    vibhag: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Clap structure: comma-separated positions of sam(1), tali, khali(0)
    sam_beats: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Carnatic jati: chatusra(4), tisra(3), misra(7), khanda(5), sankeerna(9)
    jati: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Carnatic anga breakdown: laghu count + drutam + anudrutam
    anga_structure: Mapped[str | None] = mapped_column(Text, nullable=True)

    # e.g. "vilambit, madhya, drut"
    common_tempos: Mapped[str | None] = mapped_column(String(255), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Relationships
    tracks: Mapped[list[Track]] = relationship(
        "Track", back_populates="tala_obj", foreign_keys="Track.tala_id"
    )
    compositions: Mapped[list[Composition]] = relationship(
        "Composition", back_populates="tala_obj", foreign_keys="Composition.tala_id"
    )

    def __repr__(self) -> str:
        return f"<Tala id={self.id} name={self.name!r} beats={self.beats}>"
