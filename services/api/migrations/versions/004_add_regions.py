"""Add regions table and wire to musical_traditions

Revision ID: 004
Revises: 003
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # regions
    # ------------------------------------------------------------------ #
    op.create_table(
        "regions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("continent", sa.String(64), nullable=True),
        sa.Column("country_name", sa.String(255), nullable=True),
        sa.Column("state", sa.String(255), nullable=True),
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

    op.create_index("idx_regions_continent", "regions", ["continent"])
    op.create_index("idx_regions_deleted_at", "regions", ["deleted_at"])

    # ------------------------------------------------------------------ #
    # Wire musical_traditions → regions
    # ------------------------------------------------------------------ #
    op.add_column(
        "musical_traditions",
        sa.Column(
            "region_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("regions.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index(
        "idx_musical_traditions_region_id", "musical_traditions", ["region_id"]
    )


def downgrade() -> None:
    op.drop_index("idx_musical_traditions_region_id", table_name="musical_traditions")
    op.drop_column("musical_traditions", "region_id")

    op.drop_index("idx_regions_deleted_at", table_name="regions")
    op.drop_index("idx_regions_continent", table_name="regions")
    op.drop_table("regions")
