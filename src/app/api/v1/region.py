from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user, verify_admin_acc
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_region import crud_region 
from ...schemas.region import RegionRead, RegionCreate, RegionCreateInternal, RegionUpdate, RegionUpdateInternal, RegionReadInternal 

router = APIRouter(tags=["Region"])


@router.post("/region", response_model=RegionReadInternal, status_code=201)
async def create_region(
    request: Request, 
    new_region:RegionCreate, 
    db: Annotated[AsyncSession, Depends(async_get_db)],
    dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> RegionReadInternal:
    try:
        created_new_region = await crud_region.create(db=db, object=new_region)
        return created_new_region
    except Exception as e:
        print(e)
        raise ServerErrorException(str(e))

@router.get("/regions",response_model=PaginatedListResponse[RegionReadInternal])
async def get_regions(
    request: Request, 
    db: Annotated[AsyncSession, Depends(async_get_db)], 
    dependencies: Annotated[None,Depends(verify_admin_acc)],
    page: int = 1, 
    items_per_page: int = 10
) -> dict:
    try:
        region_data = await crud_region.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=RegionReadInternal,
            is_deleted=False,
        )

        response: dict[str, Any] = paginated_response(crud_data=region_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))

@router.patch("/region/{region_id}")
async def patch_region(
    request: Request,
    values: RegionUpdate, 
    region_id: int,
    dependencies: Annotated[None,Depends(verify_admin_acc)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    try:
        db_region = await crud_region.get(db=db, schema_to_select=RegionRead,region_id=region_id)
        if not db_region:
            raise NotFoundException("Region not found")

        await crud_region.update(db=db, region_id=region_id, object=values)
        return {"message": "Region updated"}
    except NotFoundException as e:
        raise NotFoundException("Region not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))


@router.delete("/region/{region_id}")
async def erase_region(
    request: Request,
    region_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
     dependencies: Annotated[None,Depends(verify_admin_acc)]
) -> dict[str, str]:
    try:
        db_region = await crud_region.get(db=db, schema_to_select=RegionRead,region_id=region_id)
        if not db_region:
            raise NotFoundException("Region not found")

        await crud_region.remove(db=db, region_id=region_id)
        return {"message": "Region deleted"}
    except NotFoundException as e:
        raise NotFoundException("Region not found")
    except Exception as e:
        print(str(e))
        raise ServerErrorException(str(e))
