from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Float, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Loan_type(Base):
    __tablename__ = 'Loan_type'

    loan_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    loan_type_name: Mapped[str] = mapped_column(String(50), nullable=False)
    max_interest: Mapped[float] = mapped_column(Float, nullable=True)
    loan_term: Mapped[int] = mapped_column(Integer, nullable=False)
    has_mortgage: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cus_type: Mapped[int] = mapped_column(Integer, ForeignKey("Cus_type.cus_type_id", ondelete = 'CASCADE'),nullable=False)
    loan_type_describing:  Mapped[str] = mapped_column(Text, nullable=False)
    absolute_borrowing_limit: Mapped[float] = mapped_column(Float, nullable=False)
    type_of_interest:Mapped[int] = mapped_column(Integer, nullable=False)
    min_amount: Mapped[float] = mapped_column(Float, nullable=False)
    relative_borrowing_limit: Mapped[float] = mapped_column(Float, nullable=False)
    min_interest: Mapped[float] = mapped_column(Float, nullable=False)
    image: Mapped[str] = mapped_column(String, nullable=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)