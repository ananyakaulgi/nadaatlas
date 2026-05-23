"""Add composers table

Revision ID: 008
Revises: 007
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # composers
    #
    # Deliberately no FK to artists. When a composer is also a performer,
    # the overlap is resolved at the application layer by matching on the
    # shared wikidata_id or musicbrainz_id — same approach used by MusicBrainz.
    # This avoids cross-table FK constraints between sibling tables.
    # ------------------------------------------------------------------ #
    op.create_table(
        "composers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("name_native", sa.String(512), nullable=True),
        sa.Column("name_sort", sa.String(255), nullable=True),
        sa.Column(
            "tradition_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("musical_traditions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        # Broad historical era e.g. "Medieval", "Classical", "Contemporary", "Film"
        sa.Column("era", sa.String(64), nullable=True),
        sa.Column("born", sa.Date, nullable=True),
        sa.Column("died", sa.Date, nullable=True),
        sa.Column("birth_place", sa.String(255), nullable=True),
        sa.Column("nationality", sa.String(255), nullable=True),
        sa.Column("biography", sa.Text, nullable=True),
        sa.Column("biography_short", sa.String(500), nullable=True),
        # External IDs — used to cross-reference with artists table at app layer
        sa.Column("musicbrainz_id", sa.String(36), unique=True, nullable=True),
        sa.Column("wikidata_id", sa.String(64), unique=True, nullable=True),
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
        sa.Column("image_url", sa.String(1024), nullable=True),
        sa.Column("website_url", sa.String(1024), nullable=True),
        sa.Column(
            "is_verified",
            sa.Boolean,
            nullable=False,
            server_default=sa.false(),
        ),
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

    op.create_index("idx_composers_name", "composers", ["name"])
    op.create_index("idx_composers_wikidata_id", "composers", ["wikidata_id"])
    op.create_index("idx_composers_musicbrainz_id", "composers", ["musicbrainz_id"])
    op.create_index("idx_composers_tradition_id", "composers", ["tradition_id"])
    op.create_index("idx_composers_deleted_at", "composers", ["deleted_at"])


def downgrade() -> None:
    op.drop_index("idx_composers_deleted_at", table_name="composers")
    op.drop_index("idx_composers_tradition_id", table_name="composers")
    op.drop_index("idx_composers_musicbrainz_id", table_name="composers")
    op.drop_index("idx_composers_wikidata_id", table_name="composers")
    op.drop_index("idx_composers_name", table_name="composers")
    op.drop_table("composers")
