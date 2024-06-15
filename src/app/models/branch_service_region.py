from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class BranchServiceRegion(Base):
    __tablename__ = 'Branch_service_region'

    region_id : Mapped[int] =  mapped_column(Integer,ForeignKey("Region.region_id"), primary_key = True )
    branch_id : Mapped[int] =  mapped_column(Integer, ForeignKey("Branch.branch_id"), primary_key = True)
