from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .composition import Composition
    from .tradition import MusicalTradition


class Composer(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """
    A Composer is distinct from an Artist (performer).
    When a person is both (e.g. Ravi Shankar), two records exist — one in
    each table. The overlap is resolved at the application layer by matching
    on the shared wikidata_id or musicbrainz_id. No FK between the two tables.
    """

    __tablename__ = "composers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    name_native: Mapped[str | None] = mapped_column(String(512), nullable=True)
    name_sort: Mapped[str | None] = mapped_column(String(255), nullable=True)

    tradition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("musical_traditions.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Broad era e.g. "Medieval", "Classical", "Baroque", "Romantic", "Contemporary", "Film"
    era: Mapped[str | None] = mapped_column(String(64), nullable=True)

    born: Mapped[date | None] = mapped_column(Date, nullable=True)
    died: Mapped[date | None] = mapped_column(Date, nullable=True)
    birth_place: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(255), nullable=True)

    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    biography_short: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # External IDs — used to cross-reference with artists table at application layer
    musicbrainz_id: Mapped[str | None] = mapped_column(
        String(36), unique=True, nullable=True
    )
    wikidata_id: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True
    )
    wikipedia_slug: Mapped[str | None] = mapped_column(String(512), nullable=True)

    image_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Relationships
    tradition: Mapped[MusicalTradition | None] = relationship(
        "MusicalTradition", back_populates="composers", foreign_keys=[tradition_id]
    )
    compositions: Mapped[list[Composition]] = relationship(
        "Composition", back_populates="composer"
    )

    def __repr__(self) -> str:
        return f"<Composer id={self.id} name={self.name!r}>"
