from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base

class Cus_account(Base):
    __tablename__ = 'Cus_account'

    cus_account_id: Mapped[int] = mapped_column('cus_account_id',Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    account_type: Mapped[int] = mapped_column(Integer, ForeignKey("Account_type.account_type_id",ondelete='CASCADE'),nullable=False)
    cus_type: Mapped[int] = mapped_column(Integer, ForeignKey("Cus_type.cus_type_id",ondelete='CASCADE'), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer,  ForeignKey("Customer.customer_id",ondelete='CASCADE'), nullable=False) 
    

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)