"""Add openopus_id to composers and compositions tables.

Revision ID: 013
Revises: 012
Create Date: 2026-05-25
"""
from __future__ import annotations

from typing import Union

import sqlalchemy as sa
from alembic import op

revision: str = "013"
down_revision: Union[str, None] = "012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "composers",
        sa.Column("openopus_id", sa.String(16), nullable=True),
    )
    op.create_index(
        "ix_composers_openopus_id",
        "composers",
        ["openopus_id"],
        unique=True,
    )

    op.add_column(
        "compositions",
        sa.Column("openopus_id", sa.String(128), nullable=True),
    )
    op.create_index(
        "ix_compositions_openopus_id",
        "compositions",
        ["openopus_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_compositions_openopus_id", table_name="compositions")
    op.drop_column("compositions", "openopus_id")

    op.drop_index("ix_composers_openopus_id", table_name="composers")
    op.drop_column("composers", "openopus_id")
