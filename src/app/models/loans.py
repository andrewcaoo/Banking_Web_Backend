from sqlalchemy import ForeignKey, Integer,  String, Date, Boolean, DateTime, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import UTC, datetime
from ..core.db.database import Base

class Loans(Base):
    __tablename__ = 'Loans'

    loan_id: Mapped[int] = mapped_column('loan_id',autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)
    employee_id: Mapped[int|None] = mapped_column(Integer, ForeignKey('Employee.employee_id', ondelete='CASCADE'), nullable=True)
    client_account_id: Mapped[int|None] = mapped_column(Integer, ForeignKey('Cus_account.cus_account_id',ondelete = 'CASCADE'),nullable=True)
    loan_type_id: Mapped[int|None] = mapped_column(Integer, ForeignKey('Loan_type.loan_type_id', ondelete = 'CASCADE'), nullable=False)
    loan_amount: Mapped[float] = mapped_column(Float,CheckConstraint('loan_amount > 0'), nullable=False)
    date_of_approval: Mapped[Date] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    number_of_terms: Mapped[int] = mapped_column(Integer, nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    payment_type: Mapped[int] = mapped_column(Integer, nullable=False)
    proof: Mapped[str] = mapped_column(String, nullable=False)
    interest: Mapped[float] = mapped_column(Float, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)