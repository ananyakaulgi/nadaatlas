"""Add instrument_family column to instruments

Revision ID: 006
Revises: 005
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Plain listener-facing family alongside the scholarly Hornbostel-Sachs code.
    # Values: Stringed, Wind, Brass, Percussion, Keyboard, Electronic
    op.add_column(
        "instruments",
        sa.Column("instrument_family", sa.String(64), nullable=True),
    )
    op.create_index("idx_instruments_family", "instruments", ["instrument_family"])


def downgrade() -> None:
    op.drop_index("idx_instruments_family", table_name="instruments")
    op.drop_column("instruments", "instrument_family")
