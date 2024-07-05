from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, ForbiddenException, NotFoundException, ServerErrorException
from ...core.security import blacklist_token, get_password_hash, oauth2_scheme
from ...crud.crud_rate_limit import crud_rate_limits
from ...crud.crud_tier import crud_tiers
from ...crud.crud_base_account import crud_base_account
from ...models.tier import Tier
from ...schemas.tier import TierRead
from ...schemas.base_account import BaseAccountRead, BaseAccountCreate, BaseAccountCreateInternal, BaseAccountUpdate, BaseAccountReadInternal
from ...core.constants import account_permission

router = APIRouter(tags=["Base_account"])


@router.post("/base_account", response_model=BaseAccountRead, status_code=201)
async def create_user(
    request: Request, base_account: BaseAccountCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> BaseAccountRead:
    try:
        email_row = await crud_base_account.exists(db=db, email=base_account.email)
  
        if email_row:
            raise DuplicateValueException("Email is already registered")

        username_row = await crud_base_account.exists(db=db, username=base_account.username)
    
        if username_row:
            raise DuplicateValueException("Username not available")

        # check the foreign key constraint.
        user_internal_dict = base_account.model_dump()
        user_internal_dict["password"] = get_password_hash(password=user_internal_dict["password"])
        # del user_internal_dict["password"]
        
        base_account_internal = BaseAccountCreate(**user_internal_dict)
        created_base_account = await crud_base_account.create(db=db, object=base_account_internal)
        return created_base_account
    except DuplicateValueException as in_Ex:
        raise DuplicateValueException(str(in_Ex))
    except Exception as e:
        print('------>',str(e))
        raise ServerErrorException(str(e))


@router.get("/base_account", response_model=PaginatedListResponse[BaseAccountRead])
async def get_base_account_users(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    try:
        base_account_data = await crud_base_account.get_multi(
            db=db,
            offset=compute_offset(page, items_per_page),
            limit=items_per_page,
            schema_to_select=BaseAccountRead,
            is_deleted=False,
        )

        response: dict[str, Any] = paginated_response(crud_data=base_account_data, page=page, items_per_page=items_per_page)
        return response
    except Exception as e:
        print('------>',str(e))
        raise ServerErrorException(str(e))



@router.get("/base_account/me/", response_model=BaseAccountRead)
async def get_yourself(request: Request, current_user: Annotated[BaseAccountRead, Depends(get_current_user)]) -> BaseAccountRead:
    return current_user


@router.get("/base_account/{username}", response_model=BaseAccountRead)
async def read_user(request: Request, username: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    try:
        db_user: BaseAccountRead | None = await crud_base_account.get(
            db=db, schema_to_select=BaseAccountRead, username=username, is_deleted=False
        )
        if db_user is None:
            raise NotFoundException("User not found")

        return db_user
    except Exception as e:
        print('------>',str(e))
        raise ServerErrorException(str(e))

@router.patch("/base_account/{username}")
async def patch_base_account(
    request: Request,
    values: BaseAccountUpdate, 
    username: str,
    current_user: Annotated[BaseAccountRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    try:
        db_acc = await crud_base_account.get(db=db, schema_to_select=BaseAccountReadInternal, username=username)
        if db_acc is None:
            raise NotFoundException("Account not found")

        if db_acc["username"] != current_user["username"]:
            if current_user["permission"] != account_permission['admin']:
                print(current_user["permission"])
                raise ForbiddenException()

        if values.username != db_acc["username"]:
            existing_username = await crud_base_account.exists(db=db, username=values.username)
            if existing_username:
                raise DuplicateValueException("Username not available")

        if values.email != db_acc["email"]:
            existing_email = await crud_base_account.exists(db=db, email=values.email)
            if existing_email:
                raise DuplicateValueException("Email is already registered")
        update_values = values.model_dump()

        if update_values['password'] is not None:         
            update_values['password'] = get_password_hash(password=update_values['password'])
        else:
            update_values['password'] = db_acc['password']

        completed_update_value = BaseAccountUpdate(**update_values)

        await crud_base_account.update(db=db, object=completed_update_value, username=username)
        return {"message": "Account updated"}
    except NotFoundException:
        raise NotFoundException("Account not found")
    except ForbiddenException:
        raise ForbiddenException
    except DuplicateValueException as in_ve:
        raise DuplicateValueException(str(in_ve))
    except Exception as e:
        print('------>',str(e))
        raise ServerErrorException(str(e))


@router.delete("/base_account/{username}")
async def erase_base_account(
    request: Request,
    username: str,
    current_user: Annotated[BaseAccountRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    token: str = Depends(oauth2_scheme),
) -> dict[str, str]:
    try:
        db_acc = await crud_base_account.get(db=db, schema_to_select=BaseAccountRead, username=username)
        if not db_acc:
            raise NotFoundException()

        if username != current_user["username"]:
            if current_user["permission"] != account_permission['admin']:
                raise ForbiddenException()

        await crud_base_account.delete(db=db, username=username)
        await blacklist_token(token=token, db=db)
        return {"message": "Account deleted"}
    except NotFoundException:
        raise NotFoundException("Account not found")
    except Exception as e:
        print('------>',str(e))
        raise ServerErrorException(str(e))
