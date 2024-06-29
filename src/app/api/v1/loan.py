from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_loan import crud_loan 
from ...schemas.loan import LoanRead, LoanCreate, LoanCreateInternal, LoanUpdate, LoanUpdateInternal, LoanReadInternal 
from ..dependencies import verify_admin_employee, verify_admin_acc
router = APIRouter(tags=["Loan"])


@router.post("/loan", response_model=LoanCreate, status_code=201)
async def create_loan(
    request: Request,
    new_loan: LoanCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> LoanRead: 

    created_new_loan = await crud_loan.create(db=db, object=new_loan)
    return created_new_loan

@router.get("/loans",response_model=PaginatedListResponse[LoanReadInternal])
async def get_loan(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    loan_data = await crud_loan.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=LoanReadInternal,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=loan_data, page=page, items_per_page=items_per_page)
    return response

@router.get("/loan/{loan_id}", response_model=LoanReadInternal)
async def get_loan_by_id(
    request: Request, 
    loan_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> dict:
    db_loan: LoanReadInternal | None = await crud_loan.get(
        db=db, 
        schema_to_select=LoanReadInternal,
        customer_id=loan_id, 
        is_deleted=False
    )
    if db_loan is None:
        raise NotFoundException("Loan not found")

    return db_loan

@router.patch("/loan/{loan_id}")
async def path_loan(
    request: Request,
    values: LoanUpdate, 
    loan_id: int,
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_loan = await crud_loan.get(db=db, schema_to_select=LoanReadInternal, loan_id=loan_id)
    if db_loan is None:
        raise NotFoundException("Loan not found")

    await crud_loan.update(db=db, object=values, loan_id=loan_id)
    return {"message": "Loan updated"}


@router.delete("/loan/{loan_id}")
async def erase_customer(
    request: Request,
    loan_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> dict[str, str]:
    db_loan = await crud_loan.get(db=db, schema_to_select=LoanReadInternal, loan_id=loan_id)
    if not db_loan:
        raise NotFoundException("Loan not found")

    await crud_loan.delete(db=db, loan_id=loan_id)
    return {"message": "Loan deleted"}
