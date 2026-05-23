from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .artist import Artist
    from .album import Album


class Genre(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    artist_genres: Mapped[list[ArtistGenre]] = relationship(
        "ArtistGenre", back_populates="genre"
    )
    album_genres: Mapped[list[AlbumGenre]] = relationship(
        "AlbumGenre", back_populates="genre"
    )

    def __repr__(self) -> str:
        return f"<Genre id={self.id} name={self.name!r}>"


class ArtistGenre(Base):
    __tablename__ = "artist_genres"

    artist_id: Mapped[UUID] = mapped_column(
        ForeignKey("artists.id", ondelete="CASCADE"),
        primary_key=True,
    )
    genre_id: Mapped[UUID] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Relationships
    artist: Mapped[Artist] = relationship("Artist", back_populates="artist_genres")
    genre: Mapped[Genre] = relationship("Genre", back_populates="artist_genres")


class AlbumGenre(Base):
    __tablename__ = "album_genres"

    album_id: Mapped[UUID] = mapped_column(
        ForeignKey("albums.id", ondelete="CASCADE"),
        primary_key=True,
    )
    genre_id: Mapped[UUID] = mapped_column(
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True,
    )

    # Relationships
    album: Mapped[Album] = relationship("Album", back_populates="album_genres")
    genre: Mapped[Genre] = relationship("Genre", back_populates="album_genres")
