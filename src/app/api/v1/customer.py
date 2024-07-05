from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_customer import crud_customer 
from ...schemas.customer import CustomerRead, CustomerCreate, CustomerCreateInternal, CustomerUpdate, CustomerUpdateInternal, CustomerReadInternal 
from ..dependencies import verify_admin_employee
router = APIRouter(tags=["Customer"])


@router.post("/customer", response_model=CustomerReadInternal, status_code=201)
async def create_customer(
    request: Request,
    new_customer:CustomerCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> CustomerReadInternal: 
    try:
        customer_row = await crud_customer.exists(db=db, id_number=new_customer.id_number)

        if customer_row:
            raise DuplicateValueException()

        create_new_customer = await crud_customer.create(db=db, object=new_customer)
        print(create_new_customer)
        return create_new_customer
    except DuplicateValueException:
        raise DuplicateValueException("Customer' id number already existing")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.get("/customers",response_model=PaginatedListResponse[CustomerReadInternal])
async def get_customers(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        cus_data = await crud_customer.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=CustomerReadInternal,
            is_deleted=False,
        )

        response: dict[str, Any] = paginated_response(crud_data=cus_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

@router.get("/customer/{customer_id}", response_model=CustomerRead)
async def get_customer_by_id(
    request: Request, 
    customer_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> dict:
    try:
        db_cus: CustomerRead | None = await crud_customer.get(
            db=db, 
            schema_to_select=CustomerRead,
            customer_id=customer_id, 
            is_deleted=False
        )
        if db_cus is None:
            raise NotFoundException()

        return db_cus
    except NotFoundException:
        raise NotFoundException("Customer not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
        

@router.patch("/customer/{customer_id}")
async def path_customer(
    request: Request,
    values: CustomerUpdate, 
    customer_id: int,
    dependencies: Annotated[None,Depends(verify_admin_employee)],
    db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    try:
        db_customer = await crud_customer.get(db=db, schema_to_select=CustomerReadInternal,customer_id=customer_id)
        if not db_customer:
            raise NotFoundException()

        await crud_customer.update(db=db, customer_id=customer_id, object=values)
        return {"message": "Customer updated"}
    except NotFoundException:
        raise NotFoundException("Customer not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.delete("/customer/{customer_id}")
async def erase_customer(
    request: Request,
    customer_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_employee)]
) -> dict[str, str]:
    try:
        db_customer = await crud_customer.get(db=db, schema_to_select=CustomerReadInternal,customer_id=customer_id)
        if not db_customer:
            raise NotFoundException()

        await crud_customer.delete(db=db,customer_id=customer_id)
        return {"message": "Customer deleted"}
    except NotFoundException:
        raise NotFoundException("Customer not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
