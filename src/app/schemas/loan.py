from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class LoanBase(BaseModel):
    loan_type_id: Annotated[int, Field(examples=[1])]
    loan_amount: Annotated[float, Field(gt=0, examples=[1000000])]
    duration: Annotated[int, Field(gt=6, examples=[24])]
    number_of_terms: Annotated[int,Field(gte=1, examples=[2])]
    status:Annotated[int, Field(examples=[0], default=0)]
    proof: Annotated[str, Field(min_length=5, max_length=35, pattern=r"^.{5,300}$", examples=["https://i.sstatic.net/l60Hf.png"], default="https://i.sstatic.net/l60Hf.png")]
    payment_type: Annotated[int, Field(examples=[1])]
    interest: Annotated[float, Field(gt=0, examples=[30])]

class Loan(TimestampSchema, LoanBase, UUIDSchema, PersistentDeletion):
    employee_id: Annotated[int | None, Field(examples=[1])]
    client_account_id:  Annotated[int | None, Field(examples=[1])]
    date_of_approval: Annotated[datetime | None, Field(examples=[datetime.now()])]
    expiry_date: Annotated[datetime | None, Field(examples=[datetime.now()])]


# Returned value.
class LoanRead(LoanBase):
    employee_id: Annotated[int | None, Field(examples=[1])]
    client_account_id:  Annotated[int | None, Field(examples=[1])]
    date_of_approval: Annotated[datetime | None, Field(examples=[datetime.now()])]
    expiry_date: Annotated[datetime | None, Field(examples=[datetime.now()])]

class LoanReadInternal(LoanRead):
    loan_id : int

class LoanCreate(LoanBase):
    employee_id: Annotated[int | None, Field(examples=[1])]
    client_account_id:  Annotated[int | None, Field(examples=[1])]
    date_of_approval: Annotated[datetime | None, Field(examples=[datetime.now()])]
    expiry_date: Annotated[datetime | None, Field(examples=[datetime.now()])]


class LoanCreateInternal(LoanCreate):
    employee_id: Annotated[int, Field(examples=[1])]
    client_account_id:  Annotated[int, Field(examples=[1])]
    date_of_approval: Annotated[datetime , Field(examples=[datetime.now()])]
    expiry_date: Annotated[datetime, Field(examples=[datetime.now()])]
    
    created_at: datetime = Field(default_factory=datetime.now)


class LoanUpdate(LoanBase):
    model_config = ConfigDict(extra="forbid")


class LoanUpdateInternal(LoanUpdate):
    updated_at: datetime

class LoanDelete(LoanBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class LoanRestoreDeleted(LoanBase):
    is_deleted: bool
