from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..core.db.database import Base

class Loans(Base):
    __tablename__ = 'Loans'

    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    employee_ID: Mapped[int] = mapped_column(Integer, ForeignKey('Employee.employee_id'), nullable=False)
    client_account_ID: Mapped[int] = mapped_column(Integer, ForeignKey('Cus_Account.cus_account_id'),nullable=False)
    loan_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('Loan_type.loan_type_id'), nullable=False)
    loan_amount: Mapped[str] = mapped_column(String(50), nullable=False)
    submission_date: Mapped[Date] = mapped_column(Date, nullable=False)
    date_of_approval: Mapped[Date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_complete: Mapped[bool] = mapped_column(Boolean, nullable=False)