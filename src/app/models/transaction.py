from datetime import UTC, datetime
from sqlalchemy import DateTime, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class Transaction(Base):
    __tablename__ = 'Transaction'

    transaction_id: Mapped[int] = mapped_column("Transaction_ID", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    payment_id: Mapped[int] = mapped_column(Integer, ForeignKey('Payment.payment_id'), nullable=False)
    method: Mapped[int] = mapped_column(Integer, default=0, nullable=False)