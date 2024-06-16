from sqlalchemy import ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import UTC, datetime

from ..core.db.database import Base

class BranchServiceRegion(Base):
    __tablename__ = 'Branch_service_region'

    region_id : Mapped[int] =  mapped_column(Integer,ForeignKey("Region.region_id",ondelete='CASCADE'), primary_key = True )
    branch_id : Mapped[int] =  mapped_column(Integer, ForeignKey("Branch.branch_id",ondelete='CASCADE'), primary_key = True)


    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)