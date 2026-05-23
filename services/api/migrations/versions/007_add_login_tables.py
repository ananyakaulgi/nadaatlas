"""Add user_sessions and login_audit tables

Revision ID: 007
Revises: 006
Create Date: 2026-05-22
"""
from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ------------------------------------------------------------------ #
    # user_sessions — operational active session tracking
    # ------------------------------------------------------------------ #
    op.create_table(
        "user_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        # SHA-256 hash of the issued JWT — never the raw token
        sa.Column("token_hash", sa.String(512), nullable=False, unique=True),
        sa.Column("device", sa.String(255), nullable=True),
        sa.Column("ip_address", postgresql.INET, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        # NULL = still valid; set on logout or forced revocation
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_user_sessions_user_id", "user_sessions", ["user_id"])
    op.create_index("idx_user_sessions_revoked_at", "user_sessions", ["revoked_at"])
    op.create_index("idx_user_sessions_expires_at", "user_sessions", ["expires_at"])

    # ------------------------------------------------------------------ #
    # login_audit — immutable append-only history of every login attempt
    # ------------------------------------------------------------------ #
    op.create_table(
        "login_audit",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        # Nullable: failed attempts may not resolve to a valid user
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("email_attempted", sa.String(255), nullable=False),
        sa.Column("ip_address", postgresql.INET, nullable=True),
        sa.Column("user_agent", sa.Text, nullable=True),
        sa.Column("success", sa.Boolean, nullable=False),
        # e.g. "wrong_password", "account_locked", "totp_failed"
        sa.Column("failure_reason", sa.String(128), nullable=True),
        # No updated_at — this table is append-only, rows are never modified
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("idx_login_audit_user_id", "login_audit", ["user_id"])
    op.create_index("idx_login_audit_created_at", "login_audit", ["created_at"])
    op.create_index("idx_login_audit_success", "login_audit", ["success"])


def downgrade() -> None:
    op.drop_index("idx_login_audit_success", table_name="login_audit")
    op.drop_index("idx_login_audit_created_at", table_name="login_audit")
    op.drop_index("idx_login_audit_user_id", table_name="login_audit")
    op.drop_table("login_audit")

    op.drop_index("idx_user_sessions_expires_at", table_name="user_sessions")
    op.drop_index("idx_user_sessions_revoked_at", table_name="user_sessions")
    op.drop_index("idx_user_sessions_user_id", table_name="user_sessions")
    op.drop_table("user_sessions")
