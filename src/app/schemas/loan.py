from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class LoanBase(BaseModel):
    employee_id: Annotated[int | None, Field(examples=[1])]
    client_account_id:  Annotated[int | None, Field(examples=[1])]
    loan_type_id: Annotated[int | None, Field(examples=[1])]
    loan_amount: Annotated[float | None, Field(examples=[1000000])]
    submission_date: datetime
    date_of_approval: datetime
    expiry_date: datetime
    is_complete: bool

class Loan(TimestampSchema, LoanBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class LoanRead(LoanBase):
    pass

class LoanReadInternal(LoanRead):
    loan_id : int

class LoanCreate(LoanBase):
   pass


class LoanCreateInternal(LoanCreate):
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
