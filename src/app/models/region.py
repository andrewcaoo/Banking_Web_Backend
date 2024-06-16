from datetime import UTC, datetime
from sqlalchemy import DateTime, String, Integer , Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Region(Base):
    __tablename__ = "Region"

    region_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    region_name: Mapped[str] = mapped_column(String(100), nullable=False)
    region_area: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None, onupdate=lambda: datetime.now(UTC))



    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)