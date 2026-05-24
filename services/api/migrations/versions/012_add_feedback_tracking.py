"""Add resolved_at and resolution_note to feedback table.

Revision ID: 012
Revises: 011
Create Date: 2026-05-24
"""
from __future__ import annotations

from typing import Union

import sqlalchemy as sa
from alembic import op

revision: str = "012"
down_revision: Union[str, None] = "011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "feedback",
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "feedback",
        sa.Column("resolution_note", sa.String(1000), nullable=True),
    )
    # Index for fast admin queries
    op.create_index("ix_feedback_status", "feedback", ["status"])


def downgrade() -> None:
    op.drop_index("ix_feedback_status", table_name="feedback")
    op.drop_column("feedback", "resolution_note")
    op.drop_column("feedback", "resolved_at")
