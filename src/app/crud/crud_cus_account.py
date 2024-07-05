from fastcrud import FastCRUD

from ..models.cus_account import Cus_account
from ..schemas.cus_account import CusAccountCreateInternal, CusAccountDelete, CusAccountUpdate, CusAccountUpdateInternal 

CRUDCusAccount = FastCRUD[Cus_account, CusAccountCreateInternal, CusAccountDelete, CusAccountUpdate, CusAccountUpdateInternal]
crud_cus_account = CRUDCusAccount(Cus_account)
