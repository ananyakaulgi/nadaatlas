"""Add ragas and talas tables; wire FK columns onto tracks

Revision ID: 009
Revises: 008
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # ragas
    # ------------------------------------------------------------------ #
    op.create_table(
        "ragas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("name_native", sa.String(512), nullable=True),
        # "hindustani", "carnatic", or "both"
        sa.Column("tradition", sa.String(64), nullable=False),
        # For cross-tradition ragas (tradition = "both")
        sa.Column("hindustani_name", sa.String(255), nullable=True),
        sa.Column("carnatic_name", sa.String(255), nullable=True),
        # Hindustani classification
        sa.Column("that", sa.String(64), nullable=True),
        # Carnatic classification (1–72)
        sa.Column("melakarta_number", sa.Integer, nullable=True),
        # Scale structure
        sa.Column("arohana", sa.String(512), nullable=True),
        sa.Column("avarohana", sa.String(512), nullable=True),
        # Important notes
        sa.Column("vadi", sa.String(64), nullable=True),
        sa.Column("samvadi", sa.String(64), nullable=True),
        # Characteristic catch-phrase
        sa.Column("pakad", sa.String(512), nullable=True),
        # Performance context
        sa.Column("time_of_day", sa.String(64), nullable=True),
        sa.Column("season", sa.String(64), nullable=True),
        # Emotional quality e.g. "Shringara (love)", "Karuna (pathos)"
        sa.Column("rasa", sa.String(255), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
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
    op.create_index("idx_ragas_tradition", "ragas", ["tradition"])
    op.create_index("idx_ragas_time_of_day", "ragas", ["time_of_day"])
    op.create_index("idx_ragas_deleted_at", "ragas", ["deleted_at"])

    # ------------------------------------------------------------------ #
    # talas
    # ------------------------------------------------------------------ #
    op.create_table(
        "talas",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("name_native", sa.String(512), nullable=True),
        # "hindustani", "carnatic", or "both"
        sa.Column("tradition", sa.String(64), nullable=False),
        # Total beat count e.g. 16 for Teentaal, 8 for Adi
        sa.Column("beats", sa.Integer, nullable=False),
        # Hindustani subdivision pattern e.g. "4+4+4+4"
        sa.Column("vibhag", sa.String(255), nullable=True),
        # Clap structure: positions of sam(1), tali, khali(0)
        sa.Column("sam_beats", sa.String(255), nullable=True),
        # Carnatic jati: chatusra, tisra, misra, khanda, sankeerna
        sa.Column("jati", sa.String(64), nullable=True),
        # Carnatic anga breakdown: laghu + drutam + anudrutam
        sa.Column("anga_structure", sa.Text, nullable=True),
        # e.g. "vilambit, madhya, drut"
        sa.Column("common_tempos", sa.String(255), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
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
    op.create_index("idx_talas_tradition", "talas", ["tradition"])
    op.create_index("idx_talas_beats", "talas", ["beats"])
    op.create_index("idx_talas_deleted_at", "talas", ["deleted_at"])

    # ------------------------------------------------------------------ #
    # Wire ragas + talas onto tracks
    # The existing free-text raga/tala columns are kept as fallback during
    # the seeding + backfill period and dropped in a later migration.
    # ------------------------------------------------------------------ #
    op.add_column(
        "tracks",
        sa.Column(
            "raga_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("ragas.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column(
        "tracks",
        sa.Column(
            "tala_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("talas.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("idx_tracks_raga_id", "tracks", ["raga_id"])
    op.create_index("idx_tracks_tala_id", "tracks", ["tala_id"])


def downgrade() -> None:
    op.drop_index("idx_tracks_tala_id", table_name="tracks")
    op.drop_index("idx_tracks_raga_id", table_name="tracks")
    op.drop_column("tracks", "tala_id")
    op.drop_column("tracks", "raga_id")

    op.drop_index("idx_talas_deleted_at", table_name="talas")
    op.drop_index("idx_talas_beats", table_name="talas")
    op.drop_index("idx_talas_tradition", table_name="talas")
    op.drop_table("talas")

    op.drop_index("idx_ragas_deleted_at", table_name="ragas")
    op.drop_index("idx_ragas_time_of_day", table_name="ragas")
    op.drop_index("idx_ragas_tradition", table_name="ragas")
    op.drop_table("ragas")
