from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Customer(Base):
    __tablename__ = 'Customer'

    customer_id: Mapped[int] = mapped_column("customer_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    customer_name: Mapped[str] = mapped_column(String(35), nullable=False)
    dob: Mapped[Date] = mapped_column(Date, nullable=False)
    id_number: Mapped[str] = mapped_column(String(12), nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False) 
    credit_score: Mapped[int] = mapped_column(Integer, nullable=False, default=500)


    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)