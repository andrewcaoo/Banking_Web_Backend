from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.db.database import Base

class Payment(Base):
    __tablename__ = 'Payment'

    payment_id: Mapped[int] = mapped_column("payment_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey('Loans.loan_id', ondelete = 'CASCADE'), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)