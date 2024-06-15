from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Payment(Base):
    __tablename__ = 'Payment'

    payment_id: Mapped[int] = mapped_column("Payment_ID", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    total_amount: Mapped[float] = mapped_column(Float, nullable=False)
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey('Loan.loan_id'), nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Define relationship to Loan
    loan = relationship("Loan", back_populates="payments")
