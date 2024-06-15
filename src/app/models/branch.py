from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class Branch(Base):
    __tablename__ = "Branch"

    branch_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    branch_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    open_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    open_hour: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    close_hour: Mapped[int] = mapped_column(Integer, nullable=False, default=17)
    
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("Region.region_id"), nullable=False, default=None, init=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey("Employee.employee_id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None,  onupdate=lambda: datetime.now(UTC))
