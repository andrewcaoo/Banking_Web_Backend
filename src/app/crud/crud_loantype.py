from fastcrud import FastCRUD

from ..models.loan_type import Loan_type 
from ..schemas.loan_type import LoanTypeCreateInternal, LoanTypeDelete, LoanTypeUpdate, LoanTypeReadInternal

CRUDLoantype = FastCRUD[Loan_type, LoanTypeCreateInternal, LoanTypeDelete, LoanTypeUpdate, LoanTypeReadInternal]
crud_loan_type = CRUDLoantype(Loan_type)
