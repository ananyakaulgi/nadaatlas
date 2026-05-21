from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.album import AlbumSummary
from app.schemas.artist import ArtistSummary


class TrackBase(BaseModel):
    title: str
    title_native: str | None = None
    duration_seconds: int | None = None
    track_number: int | None = None
    musical_tradition: str | None = None
    raga: str | None = None
    tala: str | None = None
    maqam: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TrackCreate(TrackBase):
    album_id: UUID | None = None
    artist_id: UUID
    tradition_id: UUID | None = None
    musicbrainz_id: str | None = None
    youtube_url: str | None = None
    spotify_url: str | None = None


class TrackUpdate(BaseModel):
    title: str | None = None
    title_native: str | None = None
    duration_seconds: int | None = None
    track_number: int | None = None
    musical_tradition: str | None = None
    raga: str | None = None
    tala: str | None = None
    maqam: str | None = None
    album_id: UUID | None = None
    artist_id: UUID | None = None
    tradition_id: UUID | None = None
    musicbrainz_id: str | None = None
    youtube_url: str | None = None
    spotify_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class TrackResponse(TrackBase):
    id: UUID
    album: AlbumSummary | None = None
    artist: ArtistSummary
    youtube_url: str | None = None
    spotify_url: str | None = None
    created_at: datetime
    updated_at: datetime
