from sqlalchemy import ForeignKey, Integer,  String, Date, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import UTC, datetime
from ..core.db.database import Base

class Loans(Base):
    __tablename__ = 'Loans'

    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_ID: Mapped[int] = mapped_column(Integer, ForeignKey('Employee.employee_id',ondelete = 'CASCADE'), nullable=False)
    client_account_ID: Mapped[int] = mapped_column(Integer, ForeignKey('Cus_account.cus_account_id',ondelete = 'CASCADE'),nullable=False)
    loan_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('Loan_type.loan_type_id', ondelete = 'CASCADE'), nullable=False)
    loan_amount: Mapped[str] = mapped_column(String(50), nullable=False)
    submission_date: Mapped[Date] = mapped_column(Date, nullable=False)
    date_of_approval: Mapped[Date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_complete: Mapped[bool] = mapped_column(Boolean, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)