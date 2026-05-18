from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.artist import ArtistSummary


class AlbumBase(BaseModel):
    title: str
    title_native: str | None = None
    release_date: date | None = None
    album_type: str | None = None
    musical_tradition: str | None = None
    label: str | None = None
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AlbumCreate(AlbumBase):
    artist_id: UUID
    tradition_id: UUID | None = None
    musicbrainz_id: str | None = None
    spotify_id: str | None = None


class AlbumUpdate(BaseModel):
    title: str | None = None
    title_native: str | None = None
    release_date: date | None = None
    album_type: str | None = None
    musical_tradition: str | None = None
    label: str | None = None
    description: str | None = None
    artist_id: UUID | None = None
    tradition_id: UUID | None = None
    musicbrainz_id: str | None = None
    spotify_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class AlbumResponse(AlbumBase):
    id: UUID
    artist: ArtistSummary
    cover_image_url: str | None = None
    created_at: datetime
    updated_at: datetime


class AlbumSummary(BaseModel):
    id: UUID
    title: str
    release_date: date | None = None
    cover_image_url: str | None = None

    model_config = ConfigDict(from_attributes=True)
