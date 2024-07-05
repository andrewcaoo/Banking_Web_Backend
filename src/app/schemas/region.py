from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class RegionBase(BaseModel):
    region_name:  Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,35}$", examples=["Ha Noi"])]
    region_area:  Annotated[float | None, Field(examples=[100.0])]

class Region(TimestampSchema, RegionBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class RegionRead(RegionBase):
    pass

class RegionReadInternal(RegionRead):
    region_id : int

class RegionCreate(RegionBase):
   pass


class RegionCreateInternal(RegionCreate):
    region_id : int
    created_at: datetime = Field(default_factory=datetime.now)


class RegionUpdate(RegionBase):
    model_config = ConfigDict(extra="forbid")


class RegionUpdateInternal(RegionUpdate):
    updated_at: datetime

class RegionDelete(RegionBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class RegionRestoreDeleted(RegionBase):
    is_deleted: bool
