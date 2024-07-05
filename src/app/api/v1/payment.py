from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_payment import crud_payment 
from ...schemas.payment import PaymentRead, PaymentCreate, PaymentCreateInternal, PaymentUpdate, PaymentUpdateInternal, PaymentReadInternal
from ..dependencies import verify_admin_employee, verify_admin_acc

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
        payment_data = await crud_payment.get_multi_by_id(
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
