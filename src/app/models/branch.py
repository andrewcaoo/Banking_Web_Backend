from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Branch(Base):
    __tablename__ = "Branch"

    branch_id: Mapped[int] = mapped_column('branch_id',Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, init = False)
    branch_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    
    region_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("Region.region_id",ondelete='CASCADE'), nullable=False)
    employee_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("Employee.employee_id",ondelete='CASCADE'), nullable=False)

    open_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), nullable=False)
    open_hour: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    close_hour: Mapped[int] = mapped_column(Integer, nullable=False, default=17)
    

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default_factory=None,  onupdate=lambda: datetime.now(UTC))
    

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)