from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDMixin

if TYPE_CHECKING:
    from .user import User


class UserSession(Base, UUIDMixin):
    """Active authenticated session. One row per issued JWT."""

    __tablename__ = "user_sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # SHA-256 hash of the raw JWT — never the token itself
    token_hash: Mapped[str] = mapped_column(
        String(512), nullable=False, unique=True
    )
    device: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    # NULL = still valid; set on logout or forced revocation
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="sessions")

    @property
    def is_valid(self) -> bool:
        from datetime import timezone
        now = datetime.now(timezone.utc)
        return self.revoked_at is None and self.expires_at > now

    def __repr__(self) -> str:
        return f"<UserSession id={self.id} user_id={self.user_id} valid={self.is_valid}>"


class LoginAudit(Base, UUIDMixin):
    """Immutable append-only log of every login attempt. Rows are never updated."""

    __tablename__ = "login_audit"

    # Nullable: a failed attempt with an unrecognised email has no valid user
    user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    email_attempted: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # e.g. "wrong_password", "account_locked", "totp_failed"
    failure_reason: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    # No updated_at — this table is append-only

    # Relationships
    user: Mapped[User | None] = relationship("User", back_populates="login_audit")

    def __repr__(self) -> str:
        return (
            f"<LoginAudit id={self.id} email={self.email_attempted!r} "
            f"success={self.success}>"
        )
