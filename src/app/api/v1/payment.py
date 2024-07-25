from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession
from dateutil.relativedelta import relativedelta

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_payment import crud_payment 
from ...crud.crud_loan import crud_loan
from ...schemas.loan import LoanReadInternal
from ...schemas.payment import PaymentRead, PaymentCreate, PaymentCreateInternal, PaymentUpdate, PaymentUpdateInternal, PaymentReadInternal
from ..dependencies import verify_admin_employee, verify_admin_acc
from ...core.constants import payment_type, interest_type, payment_status
from ..helper import convert_interest_by_interest_each_month

router = APIRouter(tags=["Payment"])


@router.post("/payment", response_model=PaymentReadInternal, status_code=201)
async def create_payment(
    request: Request,
    new_payment: PaymentCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> PaymentReadInternal: 
    try:
        created_new_payment = await crud_payment.create(db=db, object=new_payment)
        return created_new_payment
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.post("/create_payment_for_loan/{loan_id}", response_model=PaginatedListResponse[PaymentReadInternal], status_code=201)
async def create_payment_for_loan(
    request: Request,
    loan_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> PaymentReadInternal: 
    try:
        loan_data = await crud_loan.get(db=db,loan_id=loan_id)
        if loan_data is None:
            raise NotFoundException()

        # created_new_payment = await crud_payment.create(db=db, object=new_payment)
        # total_amount 
        # total_amoutn -> payment_type
        #  payment_type = 1: just pay the amount from the interest
        #  payment_type = 2: pay amount from the interest and principal

        months_of_a_term = loan_data['duration'] / loan_data['number_of_terms']
        if loan_data['payment_type'] == payment_type['fixed_interest']:
            date_pivot = loan_data['date_of_approval']

            for i in range(loan_data['number_of_terms']-1):
                print('-->',relativedelta(months=+(months_of_a_term)))
                date_pivot += relativedelta(months=+(months_of_a_term))
                new_payment = {}

                new_payment['total_amount'] = loan_data['interest'] * loan_data['loan_amount'] * 0.01
                new_payment['loan_id'] = loan_id
                new_payment['status'] = payment_status['pending']
                new_payment['end_date'] = date_pivot

                created_new_payment = await crud_payment.create(db=db, object=PaymentCreate(**new_payment))

            new_payment = {}
            date_pivot += relativedelta(months=+((i+1)*(months_of_a_term)))

            new_payment['total_amount'] = loan_data['interest'] * loan_data['loan_amount']*0.01 + loan_data['loan_amount']
            new_payment['loan_id'] = loan_id
            new_payment['status'] = payment_status['pending']
            new_payment['end_date'] = date_pivot

            await crud_payment.create(db=db, object=PaymentCreate(**new_payment))
        else:
            # interest for each month * to the number of months 
            date_pivot = loan_data['date_of_approval']
            stand_amount_each_term = loan_data['loan_amount'] / loan_data['number_of_terms'] 
            cur_debt = loan_data['loan_amount']
            interest_each_term = convert_interest_by_interest_each_month(loan_data['interest'],interest_type['each_year']) * (loan_data['duration'] / loan_data['number_of_terms'])
            for i in range(loan_data['number_of_terms']):
                new_payment = {}
                date_pivot += relativedelta(months=+(months_of_a_term))

                new_payment['total_amount'] = stand_amount_each_term + interest_each_term * cur_debt*0.01
                new_payment['loan_id'] = loan_id
                new_payment['status'] = payment_status['pending']
                new_payment['end_date'] = date_pivot

                created_new_payment = await crud_payment.create(db=db, object=PaymentCreate(**new_payment))
                
                cur_debt -= stand_amount_each_term

        payment_sequential = await crud_payment.get_multi(db=db, loan_id=loan_id, schema_to_select=PaymentReadInternal, is_deleted=False)
        response: dict[str, Any] = paginated_response(crud_data=payment_sequential, page=1, items_per_page=10)
        return response
    except NotFoundException:
        raise NotFoundException("Loan not found")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.get("/payments",response_model=PaginatedListResponse[PaymentReadInternal])
async def get_payment(

    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        payment_data = await crud_payment.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=PaymentReadInternal,
            is_deleted=False,
        )

        response: dict[str, Any] = paginated_response(crud_data=payment_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

@router.get("/payment/{loan_id}", response_model=PaginatedListResponse[PaymentReadInternal])
async def get_payment_by_id(
    request: Request, 
    loan_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        payment_data = await crud_payment.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=PaymentReadInternal,
            is_deleted=False,
            loan_id=loan_id
        )

        response: dict[str, Any] = paginated_response(crud_data=payment_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

@router.patch("/payment/{payment_id}")
async def path_payment(
    request: Request,
    values: PaymentUpdate, 
    payment_id: int,
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    try:
        db_payment = await crud_payment.get(db=db, schema_to_select=PaymentReadInternal, payment_id=payment_id)
        if db_payment is None:
            raise NotFoundException()

        await crud_payment.update(db=db, object=values, payment_id=payment_id)
        return {"message": "Payment updated"}
    except NotFoundException:  
        raise NotFoundException("Payment not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.delete("/payment/{payment_id}")
async def erase_payment(
    request: Request,
    payment_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> dict[str, str]:
    try:
        db_payment = await crud_payment.get(db=db, schema_to_select=PaymentReadInternal, payment_id=payment_id)
        if db_payment is None:
            raise NotFoundException()

        await crud_payment.remove(db=db, payment_id=payment_id)
        return {"message": "Payment deleted"}
    except NotFoundException:
        raise NotFoundException("Payment not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
