from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class CustomerBase(BaseModel):
    customer_name:  Annotated[str, Field(min_length=2, max_length=35, pattern=r"^.{5,35}$", examples=["Phương Nam"])]
    dob: datetime
    id_number:  Annotated[str, Field(min_length=5, max_length=35, pattern=r"^\d{12}$", examples=["036093002023"])]
    address: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["123 Hang Ma Ha Noi", "456 Cho Lon HCM", "789 TP Thai Binh"])]
    credit_score: Annotated[int, Field(ge=300, le=850, examples=[300, 600, 850])]


class Customer(TimestampSchema, CustomerBase, UUIDSchema, PersistentDeletion):
    # profile_image_url: Annotated[str, Field(default="hhttps://i.sstatic.net/l60Hf.png")]
    # password: str
    # permission: int = 0 
    # tier_id: int | None = None
    pass

# Returned value.
class CustomerRead(CustomerBase):
    pass

class CustomerReadInternal(CustomerRead):
    customer_id : int

class CustomerCreate(CustomerBase):
   pass


class CustomerCreateInternal(CustomerCreate):
    created_at: datetime = Field(default_factory=datetime.now)

class CustomerUpdate(CustomerBase):
    model_config = ConfigDict(extra="forbid")


class CustomerUpdateInternal(CustomerUpdate):
    updated_at: datetime

class CustomerDelete(CustomerBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class CustomerRestoreDeleted(CustomerBase):
    is_deleted: bool
