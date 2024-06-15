import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class BaseAccount(Base):
    __tablename__ = "Base_account"

    baseaccount_id: Mapped[int] = mapped_column("BaseAccount_ID", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    username: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String)

    profile_image_url: Mapped[str] = mapped_column(String, default="https://profileimageurl.com")
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(default_factory=uuid_pkg.uuid4, primary_key=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    ban_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_ban: Mapped[bool] = mapped_column(default=False, index=True)
    permission: Mapped[int] = mapped_column(default=0)

    # tier_id: Mapped[int | None] = mapped_column(ForeignKey("tier.id"), index=True, default=None, init=False)
