from fastcrud import FastCRUD

from ..models.base_account import BaseAccount
from ..schemas.base_account import BaseAccountCreateInternal, BaseAccountDelete, BaseAccountUpdate, BaseAccountUpdateInternal

CRUDBaseAccount = FastCRUD[BaseAccount, BaseAccountCreateInternal, BaseAccountDelete, BaseAccountUpdate, BaseAccountUpdateInternal]
crud_base_account = CRUDBaseAccount(BaseAccount)
