from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_loantype import crud_loan_type 
from ...schemas.loan_type import LoanTypeRead, LoanTypeCreate, LoanTypeReadInternal
router = APIRouter(tags=["Loan type"])

@router.get("/loan_types",response_model=PaginatedListResponse[LoanTypeReadInternal])
async def get_loan_type(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        loan_type_data = await crud_loan_type.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=LoanTypeReadInternal,
            is_deleted=False,
        )

        response: dict[str, Any] = paginated_response(crud_data=loan_type_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print('------------------------->',str(e))
        raise ServerErrorException(str(e))


@router.get("/loan_type_by_customer_type/{cus_type_id}", response_model=PaginatedListResponse[LoanTypeReadInternal])
async def get_loan_by_emp_id(
    request: Request, 
    cus_type_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        db_loan_type = await crud_loan_type.get_multi(
            db=db, 
            schema_to_select=LoanTypeReadInternal,
            cus_type=cus_type_id, 
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            is_deleted=False
        )

        response: dict[str, Any] = paginated_response(crud_data=db_loan_type, page=page, items_per_page=items_per_page)
        return response
    
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))