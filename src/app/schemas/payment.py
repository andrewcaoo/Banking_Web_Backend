from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class PaymentBase(BaseModel):
    total_amount: Annotated[float | None, Field(examples=[1000000])]
    loan_id: Annotated[int | None, Field(examples=[1])]
    end_date: datetime
    


class Payment(TimestampSchema, PaymentBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class PaymentRead(PaymentBase):
    pass

class PaymentReadInternal(PaymentRead):
    payment_id : int

class PaymentCreate(PaymentBase):
   pass


class PaymentCreateInternal(PaymentCreate):
    created_at: datetime = Field(default_factory=datetime.now)

class PaymentUpdate(PaymentBase):
    model_config = ConfigDict(extra="forbid")


class PaymentUpdateInternal(PaymentUpdate):
    updated_at: datetime

class PaymentDelete(PaymentBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class PaymentRestoreDeleted(PaymentBase):
    is_deleted: bool
