"""Add genres table with artist and album junction tables

Revision ID: 005
Revises: 004
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # genres
    # ------------------------------------------------------------------ #
    op.create_table(
        "genres",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("slug", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.Text, nullable=True),
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
    op.create_index("idx_genres_slug", "genres", ["slug"])
    op.create_index("idx_genres_deleted_at", "genres", ["deleted_at"])

    # ------------------------------------------------------------------ #
    # artist_genres  (junction)
    # ------------------------------------------------------------------ #
    op.create_table(
        "artist_genres",
        sa.Column(
            "artist_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("artists.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "genre_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("genres.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )

    # ------------------------------------------------------------------ #
    # album_genres  (junction)
    # ------------------------------------------------------------------ #
    op.create_table(
        "album_genres",
        sa.Column(
            "album_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("albums.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "genre_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("genres.id", ondelete="CASCADE"),
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("album_genres")
    op.drop_table("artist_genres")

    op.drop_index("idx_genres_deleted_at", table_name="genres")
    op.drop_index("idx_genres_slug", table_name="genres")
    op.drop_table("genres")
