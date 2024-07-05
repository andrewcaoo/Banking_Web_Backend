from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class LoanTypeBase(BaseModel):
    loan_type_name:  Annotated[str, Field(min_length=2, examples=["Vay The Chap"])]
    has_mortgage: Annotated[bool, Field(examples=[True, False])]
    cus_type: Annotated[int | None, Field(examples=[1])]
    loan_type_describing: Annotated[str, Field( default="", description="Description of the loan type")]
    type_of_interest: Annotated[int | None, Field(examples=[1])] 
    max_interest: Annotated[float | None, Field(examples=[20.0])]
    min_interest: Annotated[float | None, Field(examples=[5])]
    loan_term: Annotated[int | None, Field(examples=[12])]
    min_amount: Annotated[float | None, Field(examples=[10])]
    relative_borrowing_limit: Annotated[float | None, Field(examples=[0.85])]
    absolute_borrowing_limit: Annotated[float | None, Field(examples=[1000000])]
    image: Annotated[str | None, Field(examples=["https://i.sstatic.net/l60Hf.png"])]

class LoanType(TimestampSchema, LoanTypeBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class LoanTypeRead(LoanTypeBase):
    pass

class LoanTypeReadInternal(LoanTypeRead):
    loan_type_id : int

class LoanTypeCreate(LoanTypeBase):
   pass


class LoanTypeCreateInternal(LoanTypeCreate):
    created_at: datetime = Field(default_factory=datetime.now)

class LoanTypeUpdate(LoanTypeBase):
    model_config = ConfigDict(extra="forbid")


class LoanTypeUpdateInternal(LoanTypeUpdate):
    updated_at: datetime

class LoanTypeDelete(LoanTypeBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class LoanTypeRestoreDeleted(LoanTypeBase):
    is_deleted: bool
