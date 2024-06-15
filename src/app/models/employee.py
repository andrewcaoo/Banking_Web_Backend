from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Employee(Base):
    __tablename__ = "Employee"

    employee_id: Mapped[int] = mapped_column("BaseAccount_ID", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    citizen_id: Mapped[str] = mapped_column(String(30), unique=True)
    employee_name: Mapped[str] = mapped_column(String(30), index=True)
    branch_id: Mapped[int] = mapped_column(Integer, ForeignKey("Branch.branch_id"), nullable=False, index = True)
    dob: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    degree: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    date_of_hire: Mapped[datetime] =  mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None,  onupdate=lambda: datetime.now(UTC))
 
    # tier_id: Mapped[int | None] = mapped_column(ForeignKey("tier.id"), index=True, default=None, init=False)
