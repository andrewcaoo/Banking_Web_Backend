from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_cus_account import crud_cus_account 
from ...schemas.cus_account import CusAccountRead, CusAccountCreate, CusAccountCreateInternal, CusAccountUpdate, CusAccountUpdateInternal, CusAccountReadInternal, CusAccount 
from ..dependencies import verify_admin_employee, verify_admin_acc
router = APIRouter(tags=["Customer account"])


@router.post("/cus_account", response_model=CusAccountReadInternal, status_code=201)
async def create_customer_account(
    request: Request,
    new_cus_account: CusAccountCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> CusAccountReadInternal: 
    global created_new_cus_account
    try:
        created_new_cus_account = await crud_cus_account.create(db=db, object=new_cus_account)
        
        return created_new_cus_account
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e)) 

@router.get("/cus_accounts",response_model=PaginatedListResponse[CusAccountReadInternal])
async def get_cus_accounts(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        cus_account_data = await crud_cus_account.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=CusAccountReadInternal,
            is_deleted=False,
        )

        response: dict[str, Any] = paginated_response(crud_data=cus_account_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e)) 

@router.get("/customer_account/{cus_account_id}", response_model=CusAccountReadInternal)
async def get_loan_by_id(
    request: Request, 
    cus_account_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> dict:
    try:
        db_cus_account= await crud_cus_account.get(
            db=db, 
            schema_to_select=CusAccountReadInternal,
            cus_account_id=cus_account_id, 
            is_deleted=False
        )
        if db_cus_account is None:
            raise NotFoundException()
        
        return db_cus_account

    except NotFoundException:
        raise NotFoundException("Customer account not found")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.get("/customer_account_by_citizen_id/{citizen_id}", response_model=PaginatedListResponse[CusAccountReadInternal])
async def get_loan_by_emp_id(
    request: Request, 
    citizen_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        db_cus_acc = await crud_cus_account.get_multi(
            db=db, 
            schema_to_select=CusAccountReadInternal,
            citizen_id=citizen_id, 
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            is_deleted=False
        )
        if db_cus_acc is None:
            raise NotFoundException()

        response: dict[str, Any] = paginated_response(crud_data=db_cus_acc, page=page, items_per_page=items_per_page)
        return response
    except NotFoundException:
        raise NotFoundException("There is no customer account was found!")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.patch("/customer_account/{cus_account_id}")
async def path_customer_account(
    request: Request,
    values: CusAccountUpdate, 
    cus_account_id: int,
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    try:
        db_cus_account = await crud_cus_account.get(db=db, schema_to_select=CusAccountReadInternal, cus_account_id=cus_account_id)
        if db_cus_account is None:
            raise NotFoundException()

        await crud_cus_account.update(db=db, object=values, cus_account_id=cus_account_id)
        return {"message": " customer account was updated"}
    except NotFoundException:
        raise NotFoundException("There is no customer account was found!")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))


@router.delete("/customer_account/{cus_account_id}")
async def erase_loan(
    request: Request,
    cus_account_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> dict[str, str]:
    try:
        db_cus_account = await crud_cus_account.get(db=db, schema_to_select=CusAccountReadInternal, cus_account_id=cus_account_id)
        if not db_cus_account:
            raise NotFoundException()

        await crud_cus_account.delete(db=db, cus_account_id=cus_account_id)
        return {"message": "Customer account deleted"}
    except NotFoundException:
        raise NotFoundException("There is no customer account was found!")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))
