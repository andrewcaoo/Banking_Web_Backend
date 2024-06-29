from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_customer import crud_customer 
from ...schemas.customer import CustomerRead, CustomerCreate, CustomerCreateInternal, CustomerUpdate, CustomerUpdateInternal, CustomerReadInternal 
from ..dependencies import verify_admin_employee
router = APIRouter(tags=["Customer"])


@router.post("/customer", response_model=CustomerCreate, status_code=201)
async def create_customer(
    request: Request,
    new_customer:CustomerCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> CustomerRead: 
    customer_row = await crud_customer.exists(db=db, id_number=new_customer.id_number)
  
    if customer_row:
        raise DuplicateValueException("Customer id already existing")

    create_new_customer = await crud_customer.create(db=db, object=new_customer)
    return create_new_customer

@router.get("/customers",response_model=PaginatedListResponse[CustomerReadInternal])
async def get_customers(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    cus_data = await crud_customer.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=CustomerReadInternal,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=cus_data, page=page, items_per_page=items_per_page)
    return response

@router.get("/customer/{customer_id}", response_model=CustomerRead)
async def get_customer_by_id(
    request: Request, 
    customer_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> dict:
    db_cus: CustomerRead | None = await crud_customer.get(
        db=db, 
        schema_to_select=CustomerRead,
        customer_id=customer_id, 
        is_deleted=False
    )
    if db_cus is None:
        raise NotFoundException("Customer not found")

    return db_cus

@router.patch("/customer/{customer_id}")
async def path_customer(
    request: Request,
    values: CustomerUpdate, 
    customer_id: int,
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    db_customer = await crud_customer.get(db=db, schema_to_select=CustomerReadInternal, customer_id=customer_id)
    if db_customer is None:
        raise NotFoundException("Customer not found")

    await crud_customer.update(db=db, object=values,  customer_id=customer_id)
    return {"message": "Customer updated"}


@router.delete("/customer/{customer_id}")
async def erase_customer(
    request: Request,
    customer_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> dict[str, str]:
    db_customer = await crud_customer.get(db=db, schema_to_select=CustomerReadInternal,customer_id=customer_id)
    if not db_customer:
        raise NotFoundException("Customer not found")

    await crud_customer.delete(db=db,customer_id=customer_id)
    return {"message": "Customer deleted"}
