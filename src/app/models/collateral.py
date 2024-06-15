from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class Collateral(Base):
    __tablename__ = 'Collateral'

    collateral_id: Mapped[int] = mapped_column("Collateral_id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    name: Mapped[str] = mapped_column(String(35), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(12),nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey('Loan.loan_id'), nullable=False)

    # Define relationships
    owner = relationship("Owner", back_populates="collaterals")
    loan = relationship("Loan", back_populates="collaterals")
