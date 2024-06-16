from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean 
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Cus_type(Base):
    __tablename__ = 'Cus_type'

    cus_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cus_type_name: Mapped[str] = mapped_column(String(30), nullable=False)
    cus_type_Desc: Mapped[str] = mapped_column(String(30), nullable=False)


    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)