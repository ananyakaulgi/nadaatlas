"""Add wikipedia_slug to musical_traditions and instruments

Revision ID: 002
Revises: 001
Create Date: 2026-05-18 00:00:00.000000

"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "musical_traditions",
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
    )
    op.add_column(
        "instruments",
        sa.Column("wikipedia_slug", sa.String(512), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("instruments", "wikipedia_slug")
    op.drop_column("musical_traditions", "wikipedia_slug")
