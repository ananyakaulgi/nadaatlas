from __future__ import annotations

from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # One of: bug_report | missing_data | feature_request | general
    category: Mapped[str] = mapped_column(String(64), nullable=False)

    name:    Mapped[str | None] = mapped_column(String(255), nullable=True)
    email:   Mapped[str | None] = mapped_column(String(255), nullable=True)
    subject: Mapped[str | None] = mapped_column(String(512), nullable=True)
    message: Mapped[str]        = mapped_column(Text,        nullable=False)

    # Which page the user was on when they opened the form
    page_context: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # new | read | resolved  (for future admin use)
    status: Mapped[str] = mapped_column(String(32), default="new", nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Feedback id={self.id} category={self.category!r}>"
