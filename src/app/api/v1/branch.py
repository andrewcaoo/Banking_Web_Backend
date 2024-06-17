from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_branch import crud_branch 
from ...schemas.branch import BranchRead, BranchCreate, BranchCreateInternal, BranchUpdate, BranchUpdateInternal, BranchReadInternal 

router = APIRouter(tags=["Branch"])


@router.post("/branch", response_model=BranchCreate, status_code=201)
async def create_branch(
    request: Request, 
    new_branch:BranchCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[Depends(verify_admin_acc)]
) -> BranchRead:

    create_new_branch = await crud_branch.create(db=db, object=new_branch)
    return create_new_branch

@router.get("/branches",response_model=PaginatedListResponse[EmployeeRead])
async def get_branches(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[Depends(verify_admin_acc)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    branches_data = await crud_branch.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=BranchReadInternal,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=branches_data, page=page, items_per_page=items_per_page)
    return response

@router.get("/branch/{branch_id}", response_model=BranchRead)
async def get_branch_by_branch_id(
    request: Request, 
    branch_id: int, db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[Depends(verify_admin_acc)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    db_branch: BranchRead | None = await crud_branch.get(
        db=db, 
        schema_to_select=BranchReadInternal,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        branch_id=branch_id, 
        is_deleted=False
    )
    if db_branch is None:
        raise NotFoundException("Branch not found")

    return db_branch

@router.patch("/branch/{branch_id}")
async def patch_branch(
    request: Request,
    values: BranchUpdate, 
    branch_id: int,
    dependencies: Annotated[Depends(verify_admin_acc)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_branch = await crud_employee.get(db=db, schema_to_select=BranchReadInternal, branch_id=branch_id)
    if db_branch is None:
        raise NotFoundException("Branch not found")

    await db_branch.update(db=db, object=values, branch_id=branch_id)
    return {"message": "Branch updated"}


@router.delete("/branch/{branch_id}")
async def erase_branch(
    request: Request,
    branch_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[Depends(verify_admin_acc)]
) -> dict[str, str]:
    db_branch = await crud_branch.get(db=db, schema_to_select=BranchReadInternal,branch_id=branch_id)
    if not db_branch:
        raise NotFoundException("Branch not found")

    await crud_branch.delete(db=db, branch_id=branch_id)
    return {"message": "Branch deleted"}
