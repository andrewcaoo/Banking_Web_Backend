from fastcrud import FastCRUD

from ..models.transaction import Transaction 
from ..schemas.transaction import TransactionCreateInternal, TransactionDelete, TransactionUpdate, TransactionUpdateInternal

CRUDTransaction = FastCRUD[Transaction, TransactionCreateInternal, TransactionDelete, TransactionUpdate, TransactionUpdateInternal]
crud_transaction = CRUDTransaction(Transaction)
