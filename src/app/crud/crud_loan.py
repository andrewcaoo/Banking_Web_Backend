from fastcrud import FastCRUD

from ..models.loans import Loans 
from ..schemas.loan import LoanCreateInternal, LoanDelete, LoanUpdate, LoanUpdateInternal

CRUDLoan = FastCRUD[Loans, LoanCreateInternal, LoanDelete, LoanUpdate, LoanUpdateInternal]
crud_loan = CRUDLoan(Loans)
