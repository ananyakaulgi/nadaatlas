"""Add compositions and composition_performances tables

Revision ID: 010
Revises: 009
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # compositions
    # ------------------------------------------------------------------ #
    op.create_table(
        "compositions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("title_native", sa.String(512), nullable=True),
        sa.Column(
            "composer_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("composers.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "tradition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("musical_traditions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        # e.g. "kriti", "bandish", "thumri", "ghazal", "qawwali", "symphony", "film"
        sa.Column("composition_type", sa.String(64), nullable=True),
        sa.Column(
            "raga_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("ragas.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "tala_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("talas.id", ondelete="SET NULL"),
            nullable=True,
        ),
        # Free text for Arabic/Turkish traditions — no maqamat table yet
        sa.Column("maqam", sa.String(255), nullable=True),
        sa.Column("language", sa.String(64), nullable=True),
        sa.Column("lyrics", sa.Text, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("year_composed", sa.Integer, nullable=True),
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
        # pgvector semantic embedding — placeholder replaced below
        sa.Column("embedding", sa.Text, nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
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
    op.execute("ALTER TABLE compositions DROP COLUMN embedding")
    op.execute("ALTER TABLE compositions ADD COLUMN embedding vector(1536)")

    op.create_index("idx_compositions_composer_id", "compositions", ["composer_id"])
    op.create_index("idx_compositions_tradition_id", "compositions", ["tradition_id"])
    op.create_index("idx_compositions_raga_id", "compositions", ["raga_id"])
    op.create_index("idx_compositions_tala_id", "compositions", ["tala_id"])
    op.create_index("idx_compositions_type", "compositions", ["composition_type"])
    op.create_index("idx_compositions_deleted_at", "compositions", ["deleted_at"])

    # ------------------------------------------------------------------ #
    # composition_performances  (junction)
    #
    # Links a Track (specific recording) to the abstract Composition,
    # the performing Artist, and the Album it appears on.
    # Composite PK: (composition_id, artist_id, album_id)
    # ------------------------------------------------------------------ #
    op.create_table(
        "composition_performances",
        sa.Column(
            "composition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("compositions.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "artist_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "album_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("albums.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "track_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("tracks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("performance_year", sa.Integer, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "idx_comp_perf_track_id", "composition_performances", ["track_id"]
    )


def downgrade() -> None:
    op.drop_index("idx_comp_perf_track_id", table_name="composition_performances")
    op.drop_table("composition_performances")

    op.drop_index("idx_compositions_deleted_at", table_name="compositions")
    op.drop_index("idx_compositions_type", table_name="compositions")
    op.drop_index("idx_compositions_tala_id", table_name="compositions")
    op.drop_index("idx_compositions_raga_id", table_name="compositions")
    op.drop_index("idx_compositions_tradition_id", table_name="compositions")
    op.drop_index("idx_compositions_composer_id", table_name="compositions")
    op.drop_table("compositions")
