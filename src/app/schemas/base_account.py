from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class BaseAccountBase(BaseModel):
    # name: Annotated[str, Field(min_length=2, max_length=30, examples=["User Userson"]]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["Username"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@domain.com"])]


class BaseAccount(TimestampSchema, BaseAccountBase, UUIDSchema, PersistentDeletion):
    profile_image_url: Annotated[str, Field(default="hhttps://i.sstatic.net/l60Hf.png")]
    password: str
    permission: int = 0 
    # tier_id: int | None = None

# Returned value.
class BaseAccountRead(BaseAccountBase):
    base_account_id: int

    # name: Annotated[str, Field(min_length=2, max_length=30, examples=["User Userson"])]
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"])]
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    employee_id: Annotated[int | None, Field(examples=[1, 2, 3])]
    cus_account_id: Annotated[int | None, Field(examples=[1, 2, 3])]
    profile_image_url: str | None
    is_ban: bool
    permission: Annotated[int, Field(examples=[0,1,2])] 

class BaseAccountReadInternal(BaseAccountBase):
    password: Annotated[str | None, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]

class BaseAccountCreate(BaseAccountBase):
    model_config = ConfigDict(extra="forbid")

    password: Annotated[str, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]
    permission: Annotated[int, Field(examples=[0,1,2])] 
    username: Annotated[str, Field(min_length=2, max_length=20, pattern=r'^[a-zA-Z0-9]{6,}$', examples=["userson"])]
    email: Annotated[EmailStr, Field(examples=["userson@example.com"])]
    employee_id: Annotated[int | None, Field(examples=[1, 2, 3])]
    cus_account_id: Annotated[int | None, Field(examples=[1, 2, 3])]
    profile_image_url: str | None
    is_ban: bool


class BaseAccountCreateInternal(BaseAccountCreate):
    base_account_id: int


class BaseAccountUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # name: Annotated[str | None, Field(min_length=2, max_length=30, examples=["User Userberg"], default=None)]
    username: Annotated[
        str | None, Field(min_length=2, max_length=20, pattern=r"^[a-z0-9]+$", examples=["userson"], default=None)
    ]
    profile_image_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$", examples=["https://i.sstatic.net/l60Hf.png"], default=None
        ),
    ]
    password: Annotated[str | None, Field(pattern=r"^.{8,}|[0-9]+|[A-Z]+|[a-z]+|[^a-zA-Z0-9]+$", examples=["Str1ngst!"])]
    permission: Annotated[int, Field(examples=[0,1,2])] 
    email: Annotated[EmailStr, Field(examples=["user.userson@example.com"])]
    employee_id: Annotated[int | None, Field(examples=[1, 2, 3])]
    cus_account_id: Annotated[int | None, Field(examples=[1, 2, 3])]
    is_ban: bool
    is_deleted: bool



class BaseAccountUpdateInternal(BaseAccountUpdate):
    updated_at: datetime


# class UserTierUpdate(BaseModel):
#     tier_id: int


class BaseAccountDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class BaseAccountRestoreDeleted(BaseModel):
    is_deleted: bool
