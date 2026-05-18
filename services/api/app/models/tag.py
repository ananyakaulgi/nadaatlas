from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .artist import Artist


class Tag(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    tag_type: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Relationships
    artist_tags: Mapped[list[ArtistTag]] = relationship(
        "ArtistTag", back_populates="tag"
    )


class ArtistTag(Base):
    __tablename__ = "artist_tags"

    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    tag_id: Mapped[UUID] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Relationships
    artist: Mapped[Artist] = relationship(
        "Artist", back_populates="artist_tags"
    )
    tag: Mapped[Tag] = relationship(
        "Tag", back_populates="artist_tags"
    )
