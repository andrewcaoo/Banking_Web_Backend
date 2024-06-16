import uuid as uuid_pkg
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class BaseAccount(Base):
    __tablename__ = "Base_account"

    base_account_id:  Mapped[int] = mapped_column("base_account_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String)

    employee_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("Employee.employee_id",ondelete='CASCADE'), nullable=True)
    cus_account_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("Cus_account.cus_account_id",ondelete='CASCADE'), nullable=True)
    profile_image_url: Mapped[str] = mapped_column(String, default="https://profileimageurl.com")
   
    # uuid: Mapped[uuid_pkg.UUID] = mapped_column(default_factory=uuid_pkg.uuid4, primary_key=True, unique=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    ban_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_ban: Mapped[bool] = mapped_column(default=False, index=True)
    permission: Mapped[int] = mapped_column(default=0)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)