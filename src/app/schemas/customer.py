from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class CustomerBase(BaseModel):
    branch_name:  Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,35}$", examples=["Ha Noi"])]
    region_id:  Annotated[int | None, Field(examples=[1])]
    employee_id: Annotated[int | None, Field(examples=[1])]
    open_date: datetime
    open_hour: Annotated[int, Field(gt=8,ls=16)] 
    close_hour: Annotated[int, Field(gt=8,ls=16)]


class Customer(TimestampSchema, BaseAccountBase, UUIDSchema, PersistentDeletion):
    # profile_image_url: Annotated[str, Field(default="hhttps://i.sstatic.net/l60Hf.png")]
    # password: str
    # permission: int = 0 
    # tier_id: int | None = None
    pass

# Returned value.
class CustomerRead(CustomerBase):
    pass

class CustomerReadInternal(CustomerBaseRead):
    branch_id : int

class CustomerCreate(CustomerBase):
   pass


class CustomerCreateInternal(CustomerBaseCreate):
    created_at = datetime


class CustomerUpdate(CustomerBase):
    model_config = ConfigDict(extra="forbid")


class CustomerUpdateInternal(CustomerBaseUpdate):
    updated_at: datetime

class CustomerDelete(CustomerBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class CustomerRestoreDeleted(CustomerBase):
    is_deleted: bool
