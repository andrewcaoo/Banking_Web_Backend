from datetime import UTC, datetime
from sqlalchemy import DateTime, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Transaction(Base):
    __tablename__ = 'Transaction'

    transaction_id: Mapped[int] = mapped_column("transaction_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_id: Mapped[int] = mapped_column(Integer, ForeignKey('Payment.payment_id',ondelete='CASCADE'), nullable=False)
    method: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)