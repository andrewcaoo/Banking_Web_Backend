from datetime import UTC, datetime
from sqlalchemy import DateTime, String, Integer , Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Region(Base):
    __tablename__ = "Region"

    region_id: Mapped[int] = mapped_column('region_id',Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init = False)
    region_name: Mapped[str] = mapped_column(String(100), nullable=False)
    region_area: Mapped[float] = mapped_column(Float, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)