from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_rate_limit import crud_rate_limits
from ...crud.crud_tier import crud_tiers
from ...crud.crud_base_account import crud_base_account
from ...models.tier import Tier
from ...schemas.tier import TierRead
from ...schemas.base_account import BaseAccountRead, BaseAccountCreate, BaseAccountCreateInternal

router = APIRouter(tags=["base_account"])


@router.post("/base_account", response_model=BaseAccountRead, status_code=201)
async def create_user(
    request: Request, base_account: BaseAccountCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> BaseAccountRead:
    email_row = await crud_base_account.exists(db=db, email=base_account.email)
  
    if email_row:
        raise DuplicateValueException("Email is already registered")

    username_row = await crud_base_account.exists(db=db, username=base_account.username)
   
    if username_row:
        raise DuplicateValueException("Username not available")
    user_internal_dict = base_account.model_dump()
    user_internal_dict["password"] = get_password_hash(password=user_internal_dict["password"])
    # del user_internal_dict["password"]
    
    base_account_internal = BaseAccountCreateInternal(**user_internal_dict)
    created_base_account = await crud_base_account.create(db=db, object=base_account_internal)
    return created_base_account


@router.get("/base_account", response_model=PaginatedListResponse[BaseAccountRead])
async def get_base_account_users(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    base_account_data = await crud_base_account.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=BaseAccountRead,
        is_deleted=False,
    )

    response: dict[str, Any] = paginated_response(crud_data=base_account_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/user/me/", response_model=BaseAccountRead)
async def get_yourself(request: Request, current_user: Annotated[BaseAccountRead, Depends(get_current_user)]) -> BaseAccountRead:
    return current_user


@router.get("/user/{username}", response_model=BaseAccountRead)
async def read_user(request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_user: BaseAccountRead | None = await crud_base_account.get(
        db=db, schema_to_select=BaseAccountRead, username=username, is_deleted=False
    )
    if db_user is None:
        raise NotFoundException("User not found")

    return db_user

# @router.patch("/user/{username}")
# async def patch_user(
#     request: Request,
#     values: UserUpdate,
#     username: str,
#     current_user: Annotated[UserRead, Depends(get_current_user)],
#     db: Annotated[AsyncSession, Depends(async_get_db)],
# ) -> dict[str, str]:
#     db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username)
#     if db_user is None:
#         raise NotFoundException("User not found")

#     if db_user["username"] != current_user["username"]:
#         raise ForbiddenException()

#     if values.username != db_user["username"]:
#         existing_username = await crud_users.exists(db=db, username=values.username)
#         if existing_username:
#             raise DuplicateValueException("Username not available")

#     if values.email != db_user["email"]:
#         existing_email = await crud_users.exists(db=db, email=values.email)
#         if existing_email:
#             raise DuplicateValueException("Email is already registered")

#     await crud_users.update(db=db, object=values, username=username)
#     return {"message": "User updated"}


# @router.delete("/user/{username}")
# async def erase_user(
#     request: Request,
#     username: str,
#     current_user: Annotated[UserRead, Depends(get_current_user)],
#     db: Annotated[AsyncSession, Depends(async_get_db)],
#     token: str = Depends(oauth2_scheme),
# ) -> dict[str, str]:
#     db_user = await crud_users.get(db=db, schema_to_select=UserRead, username=username)
#     if not db_user:
#         raise NotFoundException("User not found")

#     if username != current_user["username"]:
#         raise ForbiddenException()

#     await crud_users.delete(db=db, username=username)
#     await blacklist_token(token=token, db=db)
#     return {"message": "User deleted"}


# @router.delete("/db_user/{username}", dependencies=[Depends(get_current_superuser)])
# async def erase_db_user(
#     request: Request,
#     username: str,
#     db: Annotated[AsyncSession, Depends(async_get_db)],
#     token: str = Depends(oauth2_scheme),
# ) -> dict[str, str]:
#     db_user = await crud_users.exists(db=db, username=username)
#     if not db_user:
#         raise NotFoundException("User not found")

#     await crud_users.db_delete(db=db, username=username)
#     await blacklist_token(token=token, db=db)
#     return {"message": "User deleted from the database"}


# @router.get("/user/{username}/rate_limits", dependencies=[Depends(get_current_superuser)])
# async def read_user_rate_limits(
#     request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]
# ) -> dict[str, Any]:
#     db_user: dict | None = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
#     if db_user is None:
#         raise NotFoundException("User not found")

#     if db_user["tier_id"] is None:
#         db_user["tier_rate_limits"] = []
#         return db_user

#     db_tier = await crud_tiers.get(db=db, id=db_user["tier_id"])
#     if db_tier is None:
#         raise NotFoundException("Tier not found")

#     db_rate_limits = await crud_rate_limits.get_multi(db=db, tier_id=db_tier["id"])

#     db_user["tier_rate_limits"] = db_rate_limits["data"]

#     return db_user


# @router.get("/user/{username}/tier")
# async def read_user_tier(
#     request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]
# ) -> dict | None:
#     db_user = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
#     if db_user is None:
#         raise NotFoundException("User not found")

#     db_tier = await crud_tiers.exists(db=db, id=db_user["tier_id"])
#     if not db_tier:
#         raise NotFoundException("Tier not found")

#     joined: dict = await crud_users.get_joined(
#         db=db,
#         join_model=Tier,
#         join_prefix="tier_",
#         schema_to_select=UserRead,
#         join_schema_to_select=TierRead,
#         username=username,
#     )

#     return joined


# @router.patch("/user/{username}/tier", dependencies=[Depends(get_current_superuser)])
# async def patch_user_tier(
#     request: Request, username: str, values: UserTierUpdate, db: Annotated[AsyncSession, Depends(async_get_db)]
# ) -> dict[str, str]:
#     db_user = await crud_users.get(db=db, username=username, schema_to_select=UserRead)
#     if db_user is None:
#         raise NotFoundException("User not found")

#     db_tier = await crud_tiers.get(db=db, id=values.tier_id)
#     if db_tier is None:
#         raise NotFoundException("Tier not found")

#     await crud_users.update(db=db, object=values, username=username)
#     return {"message": f"User {db_user['name']} Tier updated"}
