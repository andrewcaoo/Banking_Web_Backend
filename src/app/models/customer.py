from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base


class Customer(Base):
    __tablename__ = 'Customer'

    customer_id: Mapped[int] = mapped_column("Customer_ID", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    customer_name: Mapped[str] = mapped_column(String(35), nullable=False)
    dob: Mapped[Date] = mapped_column(Date, nullable=False)
    id_number: Mapped[str] = mapped_column(String(12), nullable=False)
    credit_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0, default=500)
    address: Mapped[str] = mapped_column(String, nullable=False) 