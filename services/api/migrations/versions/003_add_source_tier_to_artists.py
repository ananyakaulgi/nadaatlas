"""Add source_tier column to artists table.

Revision ID: 003
Revises: 002
Create Date: 2026-05-19
"""
from alembic import op
import sqlalchemy as sa

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "artists",
        sa.Column(
            "source_tier",
            sa.SmallInteger,
            nullable=False,
            server_default="1",
            comment="Data quality tier: 1=MusicBrainz, 2=Wikipedia, 3=Spotify, 9=manual",
        ),
    )


def downgrade() -> None:
    op.drop_column("artists", "source_tier")
