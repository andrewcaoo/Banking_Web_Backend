from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, Extra

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class EmployeeBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    employee_name: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,35}$", examples=["Phuong Nam"])]
    citizen_id: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^\d{12}$", examples=["036093002023"])]
    branch_id:  Annotated[int | None, Field(examples=[1])]
    dob: Annotated[datetime, Field()]
    degree: int 
    date_of_hire: datetime




class Employee(TimestampSchema, EmployeeBase, UUIDSchema, PersistentDeletion):
    # profile_image_url: Annotated[str, Field(default="hhttps://i.sstatic.net/l60Hf.png")]
    # password: str
    # permission: int = 0 
    # tier_id: int | None = None
    pass

# Returned value.
class EmployeeRead(EmployeeBase):
    pass

class EmployeeReadInternal(EmployeeRead):
    employee_id : int

class EmployeeCreate(EmployeeBase):
    model_config = ConfigDict(extra="forbid")


class EmployeeCreateInternal(EmployeeCreate):
    created_at: datetime = Field(default_factory=datetime.now)


class EmployeeUpdate(EmployeeBase):
    model_config = ConfigDict(extra="forbid")


class EmployeeUpdateInternal(EmployeeUpdate):
    updated_at: datetime

class EmployeeDelete(EmployeeBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class EmployeeRestoreDeleted(EmployeeBase):
    is_deleted: bool
