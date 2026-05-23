from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from .tradition import MusicalTradition


class Region(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "regions"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    continent: Mapped[str | None] = mapped_column(String(64), nullable=True)
    country_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    traditions: Mapped[list[MusicalTradition]] = relationship(
        "MusicalTradition", back_populates="region_obj", foreign_keys="MusicalTradition.region_id"
    )

    def __repr__(self) -> str:
        return f"<Region id={self.id} name={self.name!r}>"
