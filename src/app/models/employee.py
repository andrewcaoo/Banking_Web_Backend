from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Employee(Base):
    __tablename__ = "Employee"

    employee_id: Mapped[int] = mapped_column("employee_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    citizen_id: Mapped[str] = mapped_column(String(30), unique=True)
    employee_name: Mapped[str] = mapped_column(String(30), index=True)
    branch_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("Branch.branch_id",ondelete='CASCADE'), nullable=False)
    dob: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    degree: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    date_of_hire: Mapped[datetime] =  mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))


    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)