from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class CustomerBase(BaseModel):
    customer_name:  Annotated[str, Field(min_length=2, max_length=35, pattern=r"^.{5,35}$", examples=["Phương Nam"])]
    id_number: Annotated[str, Field(min_length=12, max_length=12,examples=["123456789012"])]

class Customer(TimestampSchema, CustomerBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class CustomerRead(CustomerBase):
    dob: Annotated[datetime| None, Field(default=None)]
    address: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["123 Hang Ma Ha Noi", "456 Cho Lon HCM", "789 TP Thai Binh"])]
    credit_score: Annotated[int | None, Field(ge=300, le=850, examples=[300, 600, 850])]
    front_of_id_card: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]
    back_of_id_card: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]
    face_video: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]

class CustomerReadInternal(CustomerRead):
    customer_id : int

class CustomerCreate(CustomerBase):
    dob: Annotated[datetime| None, Field(default=None)]
    address: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["123 Hang Ma Ha Noi", "456 Cho Lon HCM", "789 TP Thai Binh"])]
    credit_score: Annotated[int | None, Field(ge=300, le=850, examples=[300, 600, 850])]
    front_of_id_card: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]
    back_of_id_card: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]
    face_video: Annotated[str | None, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]


class CustomerCreateInternal(CustomerCreate):
    customer_id : int
    created_at: datetime = Field(default_factory=datetime.now)

class CustomerUpdate(CustomerBase):
    dob: Annotated[datetime, Field(default=None)]
    address: Annotated[str , Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["123 Hang Ma Ha Noi", "456 Cho Lon HCM", "789 TP Thai Binh"])]
    credit_score: Annotated[int, Field(ge=300, le=850, examples=[300, 600, 850])]
    front_of_id_card: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]
    back_of_id_card: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]
    face_video: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"])]


class CustomerUpdateInternal(CustomerUpdate):
    updated_at: datetime

class CustomerDelete(CustomerBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class CustomerRestoreDeleted(CustomerBase):
    is_deleted: bool
