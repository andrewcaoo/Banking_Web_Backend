from typing import Annotated, Any
from starlette.config import Config
import os
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from ...api.dependencies import login_require 
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException

from ...crud.crud_transaction import crud_transaction
from ...schemas.transaction import TransactionRead, TransactionReadInternal
from ...crud.crud_loan import crud_loan
from ...schemas.loan import LoanRead, LoanReadInternal, LoanUpdateInternal, LoanUpdateInternal, LoanStatusUpdate
from ...crud.crud_payment import crud_payment
from ...schemas.payment import PaymentRead, PaymentReadInternal, PaymentUpdate, PaymentStatusUpdate, PaymentUpdateInternal

from ...core.constants import account_permission, transaction_method, transaction_status, payment_status, loan_status


# laon transaction and payment
router = APIRouter(tags=["Update transaction and loan status"])

@router.get("/update_loan_tran_status/{loan_id}")
async def get_transaction_by_loan_id(
    request: Request, 
    loan_id: int, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(login_require)]
) -> dict:
    try:
        db_loan = await crud_loan.get(
            db=db, 
            loan_id=loan_id, 
            is_deleted=False
        )
        if db_loan is None:
            raise NotFoundException('The loan not found')

        db_payment = await crud_payment.get_multi(
            db=db, 
            loan_id=loan_id, 
            is_deleted=False
        )

        if db_payment is None:
            raise NotFoundException('The payment not found')

        # payments_id = [payment['payment_id'] for payment in db_payment['data']]
        payments = db_payment['data']

        completed_payments = 0
        for payment in payments:
            if payment['status'] == payment_status['completed']:
                completed_payments += 1
            transactions = await crud_transaction.get_multi(
                db=db, 
                payment_id=payment['payment_id'],  
                is_deleted=False
            )
            transactions = transactions['data']
            sum_amount = 0 
            for transaction in transactions:
                if transaction['status'] == transaction_status['completed']:
                   sum_amount += transaction['amount']
            if sum_amount >= payment['total_amount'] and payment['status'] != payment_status['completed']:
                completed_payments += 1
                payment_update =  PaymentStatusUpdate(
                    status = transaction_status['completed']
                )
                await crud_payment.update(db=db, object=payment_update, payment_id=payment['payment_id'])

        if completed_payments == len(payments):
            loan_update = LoanStatusUpdate(
                status = loan_status['completed']
            )
            await crud_loan.update(db=db, object=loan_update, loan_id=loan_id)

        return {
            'loan_id':loan_id,
            'status': 'Success'
        }
    except NotFoundException as nfe:
        raise  NotFoundException(str(nfe))
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

