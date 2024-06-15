from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class Cus_Account(Base):
    __tablename__ = 'Cus_Account'

    cus_account_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    account_type: Mapped[int] = mapped_column(Integer, ForeignKey("AccountType.account_type_id"), nullable=False)
    cus_type: Mapped[int] = mapped_column(Integer, ForeignKey("Cus_type.cus_type_id"), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer,  ForeignKey("Customer.customer_id"), nullable=False)  