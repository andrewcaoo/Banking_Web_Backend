from datetime import datetime
from typing import Annotated, Optional, List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class BranchSRBase(BaseModel):
    region_id:  Annotated[int | None, Field(examples=[1])]
    branch_id: Annotated[int | None, Field(examples=[1])]


class BranchSR(TimestampSchema, BranchSRBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class BranchSRRead(BranchSRBase):
    pass

class BranchSRReadInternal(BranchSRRead):
    branch_id : int

class BranchSRCreate(BranchSRBase):
   regions_list: List[int] = [] 
   pass


class BranchSRCreateInternal(BranchSRCreate):
    created_at: datetime = Field(default_factory=datetime.now)


class BranchSRUpdate(BranchSRBase):
    model_config = ConfigDict(extra="forbid")


class BranchSRUpdateInternal(BranchSRUpdate):
    updated_at: datetime

class BranchSRDelete(BranchSRBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class BranchSRRestoreDeleted(BranchSRBase):
    is_deleted: bool
