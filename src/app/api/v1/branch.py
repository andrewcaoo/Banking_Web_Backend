from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_branch import crud_branch 
from ...schemas.branch import BranchRead, CompletedBranchRead, ClientBranchCreate, BackendBranchCreate, BranchCreateInternal, BranchUpdate, BranchUpdateInternal, BranchReadInternal 
from ...crud.crud_branchSR import crud_branchSR
from ...schemas.branch_service_region import regionsList, BranchSRBase, BranchSRReadInternal, BranchSRRead, BranchSRCreateInternal, BranchSRUpdate, BranchSRUpdateInternal

router = APIRouter(tags=["Branch"])


@router.post("/branch", response_model=CompletedBranchRead, status_code=201)
async def create_branch(
    request: Request, 
    new_branch:ClientBranchCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> CompletedBranchRead:
    try:
        internal_new_branch = new_branch.model_dump()
        regions_list = internal_new_branch['regions_list']
        internal_new_branch.pop('regions_list')

        internal_branch_obj= BackendBranchCreate(**internal_new_branch)
        # get branch id
        created_new_branch = await crud_branch.create(db=db, object=internal_branch_obj)

        for region_id in regions_list:
            branch_sr = BranchSRBase(region_id=region_id, branch_id=created_new_branch.branch_id)
            await crud_branchSR.create(db=db, object=branch_sr)
        
        # Assuming `created_new_branch` is an SQLAlchemy model instance
        created_new_branch_dict = {column.name: getattr(created_new_branch, column.name) for column in created_new_branch.__table__.columns}

        returned_new_branch = CompletedBranchRead(regions_list=regions_list, **created_new_branch_dict)
        return returned_new_branch
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
    

@router.get("/branches",response_model=PaginatedListResponse[CompletedBranchRead])
async def get_branches(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_acc)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        branches_data = await crud_branch.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=BranchReadInternal,
            is_deleted=False,
        )
        for branch_index in range(len(branches_data['data'])):
            branch_id = branches_data['data'][branch_index]['branch_id']
            region_data = await crud_branchSR.get_multi(db=db, branch_id=branch_id, schema_to_select=regionsList)
            regions_list = [data['region_id'] for data in region_data['data']]
            branches_data['data'][branch_index]['regions_list'] = regions_list

        response: dict[str, Any] = paginated_response(crud_data=branches_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.get("/branch/{branch_id}", response_model=CompletedBranchRead)
async def get_branch_by_branch_id(
    request: Request, 
    branch_id: int, db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> dict:
    try:
        db_branch = await crud_branch.get(
            db=db, 
            schema_to_select=BranchReadInternal,
            branch_id=branch_id, 
            is_deleted=False
        )

        if db_branch is None:
            raise NotFoundException()

        branch_id = db_branch['branch_id']
        region_data = await crud_branchSR.get_multi(db=db, branch_id=branch_id, schema_to_select=regionsList)
        regions_list = [data['region_id'] for data in region_data['data']]
        db_branch['regions_list'] = regions_list

        return db_branch
    except NotFoundException:
        raise NotFoundException("Branch not found")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.patch("/branch/{branch_id}")
async def patch_branch(

    request: Request,
    values: BranchUpdate, 
    branch_id: int,
    dependencies: Annotated[None,Depends(verify_admin_acc)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    try:
        db_branch = await crud_branch.get(db=db, schema_to_select=BranchReadInternal, branch_id=branch_id)
        if db_branch is None:
            raise NotFoundException("Branch not found")

        internal_update_branch = values.model_dump()
        new_regions_list = internal_update_branch['regions_list']
        internal_update_branch.pop('regions_list')

        internal_branch_obj= BackendBranchCreate(**internal_update_branch)
        
        region_data = await crud_branchSR.get_multi(db=db, branch_id=branch_id, schema_to_select=regionsList)
        regions_list = [data['region_id'] for data in region_data['data']]

        new_regions_set =set(new_regions_list)
        regions_set = set(regions_list)
        own_regions = regions_set - new_regions_set
        own_new_regions = new_regions_set - regions_set

        for region_id in own_regions:
            await crud_branchSR.db_delete(db=db, branch_id=branch_id, region_id=region_id)

        for region_id in own_new_regions:
            branch_sr = BranchSRBase(region_id=region_id, branch_id=branch_id)
            await crud_branchSR.create(db=db, object=branch_sr)

        await crud_branch.update(db=db, object=internal_branch_obj, branch_id=branch_id)

        return {"message": "Branch updated"}
    except NotFoundException:
        raise NotFoundException("Branch not found")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))


@router.delete("/branch/{branch_id}")
async def erase_branch( 
    request: Request,
    branch_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
     dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> dict[str, str]:
    try:
        db_branch = await crud_branch.get(db=db, schema_to_select=BranchReadInternal,branch_id=branch_id)
        if not db_branch:
            raise NotFoundException("Branch not found")
        
        region_data = await crud_branchSR.get_multi(db=db, branch_id=branch_id, schema_to_select=regionsList)
        regions_list = [data['region_id'] for data in region_data['data']]

        for region in regions_list:
            await crud_branchSR.delete(db=db, branch_id=branch_id, region_id=region)

        await crud_branch.delete(db=db, branch_id=branch_id)
        return {"message": "Branch deleted"}
    except NotFoundException:
        raise NotFoundException("Branch not found")
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))
