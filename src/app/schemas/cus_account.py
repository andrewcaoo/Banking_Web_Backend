from datetime import datetime
from typing import Annotated, Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class CusAccountBase(BaseModel):
    account_type:  Annotated[int | None, Field(examples=[1],default=1)]
    cus_type: Annotated[int | None, Field(examples=[1],default=1)]
    customer_id: Annotated[int | None, Field(examples=[1])]


class CusAccount(TimestampSchema, CusAccountBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class CusAccountRead(CusAccountBase):
    pass

class CusAccountReadInternal(CusAccountRead):
    cus_account_id : int

class CusAccountCreate(CusAccountBase):
   pass

class CusAccountCreateInternal(CusAccountCreate):
    created_at: datetime = Field(default_factory=datetime.now)


class CusAccountUpdate(CusAccountBase):
    model_config = ConfigDict(extra="forbid")


class CusAccountUpdateInternal(CusAccountUpdate):
    updated_at: datetime

class CusAccountDelete(CusAccountBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime

class CusAccountDeleted(CusAccountBase):
    is_deleted: bool
