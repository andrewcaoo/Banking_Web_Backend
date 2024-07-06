from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc, login_require, verify_admin_employee
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_transaction import crud_transaction
from ...schemas.transaction import TransactionRead, TransactionCreate, TransactionCreateInternal, TransactionUpdate, TransactionUpdateInternal, TransactionReadInternal
from ...core.constants import account_permission

router = APIRouter(tags=["Transaction"])


@router.post("/transaction", response_model=TransactionReadInternal, status_code=201)
async def create_transaction(
    request: Request, 
    new_transaction: TransactionCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(login_require)]
) -> TransactionReadInternal:
    try:
        created_new_transaction = await crud_transaction.create(db=db, object=new_transaction)
        return created_new_transaction

    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.get("/transaction/{payment_id}", response_model=PaginatedListResponse[TransactionReadInternal])
async def get_transaction_by_loan_id(
    request: Request, 
    payment_id: int, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(login_require)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        db_transaction = await crud_transaction.get_multi(
            db=db, 
            schema_to_select=TransactionReadInternal,
            payment_id=payment_id, 
            is_deleted=False
        )
        if db_transaction is None:
            raise NotFoundException()

        response: dict[str, Any] = paginated_response(crud_data=db_transaction, page=page, items_per_page=items_per_page)
        return response
    except NotFoundException:
        raise  NotFoundException("Transaction not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.patch("/transaction/{transaction_id}")
async def patch_employee(
    request: Request,
    values: TransactionUpdate, 
    transaction_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    try:
        db_tran = await crud_transaction.get(db=db, schema_to_select=TransactionReadInternal, transaction_id=transaction_id)
        if db_tran is None:
            raise NotFoundException()

        await crud_transaction.update(db=db, object=values, transaction_id=transaction_id)
        return {"message": "Transaction updated"}
    except NotFoundException:
        raise NotFoundException("Transaction not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))



@router.delete("/transaction/{transaction_id}")
async def erase_employee(
    request: Request,
    transaction_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(verify_admin_employee)]
) -> dict[str, str]:
    try:
        db_tran = await crud_transaction.get(db=db, schema_to_select=TransactionReadInternal, transaction_id=transaction_id)
        if not db_tran:
            raise NotFoundException("Transaction not found")

        await crud_transaction.delete(db=db, transaction_id=transaction_id)
        return {"message": "Transaction deleted"}
    except NotFoundException:
        raise NotFoundException("Transaction not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
