from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_employee import crud_employee
from ...schemas.employee import EmployeeRead, EmployeeCreate, EmployeeCreateInternal, EmployeeUpdate, EmployeeUpdateInternal, EmployeeReadInternal
from ...core.constants import account_permission

router = APIRouter(tags=["Employee"])


@router.post("/employee", response_model=EmployeeReadInternal, status_code=201)
async def create_employee(
    request: Request, 
    new_employee: EmployeeCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(verify_admin_acc)]
) -> EmployeeRead:
    try:
        employee_row = await crud_employee.exists(db=db, citizen_id=new_employee.citizen_id)
  
        if employee_row:
            raise DuplicateValueException()

        created_new_employee = await crud_employee.create(db=db, object=new_employee)
        return created_new_employee
    except DuplicateValueException:
        raise DuplicateValueException("Employee's citizen_id already existing")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.get("/employees", response_model=PaginatedListResponse[EmployeeReadInternal])
async def get_employees(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None, Depends(verify_admin_acc)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        employee_data = await crud_employee.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=EmployeeReadInternal,
            is_deleted=False,
        )
        response: dict[str, Any] = paginated_response(crud_data=employee_data, page=page, items_per_page=items_per_page)

        return response
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

@router.get("/employee/{employee_id}", response_model=EmployeeReadInternal)
async def get_employee_by_employee_id(
    request: Request, 
    employee_id: int, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(verify_admin_acc)]
) -> dict:
    try:
        db_employee: EmployeeRead | None = await crud_employee.get(
            db=db, 
            schema_to_select=EmployeeReadInternal,
            employee_id=employee_id, 
            is_deleted=False
        )
        if db_employee is None:
            raise NotFoundException()

        return db_employee
    except NotFoundException:
        raise  NotFoundException("Employee not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

@router.patch("/employee/{employee_id}")
async def patch_employee(
    request: Request,
    values: EmployeeUpdate, 
    employee_id: int,
    dependencies: Annotated[None, Depends(verify_admin_acc)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    try:
        db_emp = await crud_employee.get(db=db, schema_to_select=EmployeeReadInternal, employee_id=employee_id)
        if db_emp is None:
            raise NotFoundException("Employee not found")

        if values.citizen_id != db_emp["citizen_id"]:
            existing_citizen_id = await crud_employee.exists(db=db, citizen_id=values.citizen_id)
            if existing_citizen_id:
                raise DuplicateValueException("Citizen_id is already registered")

        await crud_employee.update(db=db, object=values, employee_id=employee_id)
        return {"message": "Employee updated"}
    except NotFoundException:
        raise NotFoundException("Employee not found")
    except DuplicateValueException:
        raise DuplicateValueException("Employee's citizen_id already existing")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.delete("/employee/{employee_id}")
async def erase_employee(
    request: Request,
    employee_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None, Depends(verify_admin_acc)]
) -> dict[str, str]:
    try:
        db_emp = await crud_employee.get(db=db, schema_to_select=EmployeeReadInternal, employee_id=employee_id)
        if not db_emp:
            raise NotFoundException("Employee not found")

        await crud_employee.delete(db=db, employee_id=employee_id)
        return {"message": "Employee deleted"}
    except NotFoundException:
        raise NotFoundException("Employee not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
