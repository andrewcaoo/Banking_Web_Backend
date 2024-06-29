from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class BranchBase(BaseModel):
    branch_name:  Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,35}$", examples=["Ha Noi"])]
    region_id:  Annotated[int | None, Field(examples=[1])]
    employee_id: Annotated[int | None, Field(examples=[1])]
    open_date: datetime
    open_hour: Annotated[int, Field(gt=7,ls=16,examples=[8])] 
    close_hour: Annotated[int, Field(gt=8,ls=16,examples=[18])]


class Branch(TimestampSchema, BranchBase, UUIDSchema, PersistentDeletion):
    # profile_image_url: Annotated[str, Field(default="hhttps://i.sstatic.net/l60Hf.png")]
    # password: str
    # permission: int = 0 
    # tier_id: int | None = None
    pass

# Returned value.
class BranchRead(BranchBase):
    pass

class BranchReadInternal(BranchRead):
    branch_id : int

class BranchCreate(BranchBase):
   pass


class BranchCreateInternal(BranchCreate):
    created_at: datetime = Field(default_factory=datetime.now)


class BranchUpdate(BranchBase):
    model_config = ConfigDict(extra="forbid")


class BranchUpdateInternal(BranchUpdate):
    updated_at: datetime

class BranchDelete(BranchBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class BranchRestoreDeleted(BranchBase):
    is_deleted: bool
