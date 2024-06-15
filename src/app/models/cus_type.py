from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base


class CusType(Base):
    __tablename__ = 'Cus_type'

    cus_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cus_type_name: Mapped[str] = mapped_column(String(30), nullable=False)
    cus_type_Desc: Mapped[str] = mapped_column(String(30), nullable=False)