"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-18 00:00:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # ------------------------------------------------------------------ #
    # musical_traditions
    # ------------------------------------------------------------------ #
    op.create_table(
        "musical_traditions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("name_native", sa.String(512), nullable=True),
        sa.Column("region", sa.String(255), nullable=False),
        sa.Column("subregion", sa.String(255), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("origin_period", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # ------------------------------------------------------------------ #
    # instruments
    # ------------------------------------------------------------------ #
    op.create_table(
        "instruments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("name_native", sa.String(512), nullable=True),
        sa.Column("hornbostel_sachs", sa.String(64), nullable=True),
        sa.Column("hs_category", sa.String(64), nullable=True),
        sa.Column(
            "tradition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("musical_traditions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("origin_region", sa.String(255), nullable=True),
        sa.Column("materials", postgresql.ARRAY(sa.String), nullable=True),
        sa.Column("image_url", sa.String(1024), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # ------------------------------------------------------------------ #
    # artists
    # ------------------------------------------------------------------ #
    op.create_table(
        "artists",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("name_native", sa.String(512), nullable=True),
        sa.Column("name_sort", sa.String(255), nullable=True),
        sa.Column("musicbrainz_id", sa.String(36), unique=True, nullable=True),
        sa.Column("wikidata_id", sa.String(64), unique=True, nullable=True),
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
        sa.Column("biography", sa.Text, nullable=True),
        sa.Column("biography_short", sa.String(500), nullable=True),
        sa.Column("born", sa.Date, nullable=True),
        sa.Column("died", sa.Date, nullable=True),
        sa.Column("birth_place", sa.String(255), nullable=True),
        sa.Column("nationality", sa.String(255), nullable=True),
        sa.Column("musical_tradition", sa.String(255), nullable=True),
        sa.Column(
            "tradition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("musical_traditions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "primary_instrument_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("instruments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        # pgvector column — uses SQL DDL directly to avoid driver-level type registration issues
        sa.Column(
            "embedding",
            sa.Text,  # placeholder type; replaced by raw DDL below
            nullable=True,
        ),
        sa.Column("image_url", sa.String(1024), nullable=True),
        sa.Column("website_url", sa.String(1024), nullable=True),
        sa.Column("spotify_id", sa.String(64), nullable=True),
        sa.Column("youtube_channel_id", sa.String(64), nullable=True),
        sa.Column(
            "is_verified",
            sa.Boolean,
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    # Replace placeholder Text column with proper vector type
    op.execute("ALTER TABLE artists DROP COLUMN embedding")
    op.execute("ALTER TABLE artists ADD COLUMN embedding vector(1536)")

    # ------------------------------------------------------------------ #
    # albums
    # ------------------------------------------------------------------ #
    op.create_table(
        "albums",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("title_native", sa.String(512), nullable=True),
        sa.Column(
            "artist_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("musicbrainz_id", sa.String(36), unique=True, nullable=True),
        sa.Column("release_date", sa.Date, nullable=True),
        sa.Column("album_type", sa.String(64), nullable=True),
        sa.Column(
            "tradition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("musical_traditions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("musical_tradition", sa.String(255), nullable=True),
        sa.Column("label", sa.String(255), nullable=True),
        sa.Column("cover_image_url", sa.String(1024), nullable=True),
        sa.Column("spotify_id", sa.String(64), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # ------------------------------------------------------------------ #
    # tracks
    # ------------------------------------------------------------------ #
    op.create_table(
        "tracks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("title_native", sa.String(512), nullable=True),
        sa.Column(
            "album_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("albums.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "artist_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("musicbrainz_id", sa.String(36), unique=True, nullable=True),
        sa.Column("duration_seconds", sa.Integer, nullable=True),
        sa.Column("track_number", sa.Integer, nullable=True),
        sa.Column("musical_tradition", sa.String(255), nullable=True),
        sa.Column(
            "tradition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("musical_traditions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("raga", sa.String(255), nullable=True),
        sa.Column("tala", sa.String(255), nullable=True),
        sa.Column("maqam", sa.String(255), nullable=True),
        sa.Column("lyrics", sa.Text, nullable=True),
        sa.Column(
            "embedding",
            sa.Text,  # placeholder replaced below
            nullable=True,
        ),
        sa.Column("youtube_url", sa.String(1024), nullable=True),
        sa.Column("spotify_url", sa.String(1024), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.execute("ALTER TABLE tracks DROP COLUMN embedding")
    op.execute("ALTER TABLE tracks ADD COLUMN embedding vector(1536)")

    # ------------------------------------------------------------------ #
    # artist_instruments
    # ------------------------------------------------------------------ #
    op.create_table(
        "artist_instruments",
        sa.Column(
            "artist_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "instrument_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("instruments.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "is_primary",
            sa.Boolean,
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("proficiency", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------ #
    # tags
    # ------------------------------------------------------------------ #
    op.create_table(
        "tags",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("slug", sa.String(255), nullable=False, unique=True),
        sa.Column("tag_type", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )

    # ------------------------------------------------------------------ #
    # artist_tags
    # ------------------------------------------------------------------ #
    op.create_table(
        "artist_tags",
        sa.Column(
            "artist_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "tag_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tags.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )

    # ------------------------------------------------------------------ #
    # Indexes
    # ------------------------------------------------------------------ #
    op.create_index("idx_artists_name", "artists", ["name"])
    op.create_index("idx_artists_musicbrainz_id", "artists", ["musicbrainz_id"])
    op.create_index("idx_artists_tradition", "artists", ["musical_tradition"])
    op.create_index("idx_artists_deleted_at", "artists", ["deleted_at"])
    op.create_index("idx_tracks_artist_id", "tracks", ["artist_id"])
    op.create_index("idx_albums_artist_id", "albums", ["artist_id"])
    op.create_index("idx_instruments_hs", "instruments", ["hornbostel_sachs"])

    # ------------------------------------------------------------------ #
    # users
    # ------------------------------------------------------------------ #
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("email_verified", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("totp_secret", sa.String(512), nullable=True),
        sa.Column("totp_enabled", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("is_superuser", sa.Boolean, nullable=False, server_default=sa.false()),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("failed_login_attempts", sa.Integer, nullable=False, server_default=sa.text("0")),
        sa.Column("locked_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # ------------------------------------------------------------------ #
    # user_backup_codes
    # ------------------------------------------------------------------ #
    op.create_table(
        "user_backup_codes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("code_hash", sa.String(255), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
    )

    # ------------------------------------------------------------------ #
    # Row Level Security (scaffolding — no policies yet)
    # ------------------------------------------------------------------ #
    op.execute("ALTER TABLE artists ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE albums ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE tracks ENABLE ROW LEVEL SECURITY")


def downgrade() -> None:
    # Drop RLS
    op.execute("ALTER TABLE tracks DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE albums DISABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE artists DISABLE ROW LEVEL SECURITY")

    # Drop indexes
    op.drop_index("idx_instruments_hs", table_name="instruments")
    op.drop_index("idx_albums_artist_id", table_name="albums")
    op.drop_index("idx_tracks_artist_id", table_name="tracks")
    op.drop_index("idx_artists_deleted_at", table_name="artists")
    op.drop_index("idx_artists_tradition", table_name="artists")
    op.drop_index("idx_artists_musicbrainz_id", table_name="artists")
    op.drop_index("idx_artists_name", table_name="artists")

    # Drop tables in reverse dependency order
    op.drop_table("user_backup_codes")
    op.drop_table("users")
    op.drop_table("artist_tags")
    op.drop_table("tags")
    op.drop_table("artist_instruments")
    op.drop_table("tracks")
    op.drop_table("albums")
    op.drop_table("artists")
    op.drop_table("instruments")
    op.drop_table("musical_traditions")

    # Drop extension
    op.execute("DROP EXTENSION IF EXISTS vector")
