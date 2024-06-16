from sqlalchemy import ForeignKey, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import UTC, datetime

from ..core.db.database import Base

class Collateral(Base):
    __tablename__ = 'Collateral'

    collateral_id: Mapped[int] = mapped_column("collateral_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    name: Mapped[str] = mapped_column(String(35), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(12),nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey('Loans.loan_id',ondelete='CASCADE'), nullable=False)



    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)