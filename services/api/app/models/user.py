from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    """Internal admin/editor user. Phase 1 is single-user; schema is multi-user ready."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # TOTP — secret stored encrypted at the application layer (AES-GCM via cryptography lib)
    totp_secret: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
        default=None,
    )
    totp_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Account state
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # Session / lockout tracking
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    # Relationships
    backup_codes: Mapped[list[UserBackupCode]] = relationship(
        "UserBackupCode",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    sessions: Mapped[list] = relationship(
        "UserSession",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
    )
    login_audit: Mapped[list] = relationship(
        "LoginAudit",
        back_populates="user",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r}>"


class UserBackupCode(UUIDMixin, Base):
    """Bcrypt-hashed TOTP backup codes. Each code is single-use."""

    __tablename__ = "user_backup_codes"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Stored as a bcrypt hash — never the raw code
    code_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    # Relationships
    user: Mapped[User] = relationship("User", back_populates="backup_codes")

    def __repr__(self) -> str:
        return f"<UserBackupCode id={self.id} user_id={self.user_id} used={self.used_at is not None}>"
