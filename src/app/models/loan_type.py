from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Loan_type(Base):
    __tablename__ = 'Loan_type'

    loan_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    loan_type_name: Mapped[str] = mapped_column(String(50), nullable=False)
    interest: Mapped[float] = mapped_column(Float, nullable=False)
    loan_term: Mapped[int] = mapped_column(Integer, nullable=False)
    has_mortgage: Mapped[bool] = mapped_column(Boolean, nullable=False)
    cus_type: Mapped[int] = mapped_column(Integer, ForeignKey("Cus_type.cus_type_id", ondelete = 'CASCADE'),nullable=False)


    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)