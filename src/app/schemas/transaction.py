from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, Extra
from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class TransactionBase(BaseModel):
    amount: Annotated[float, Field(gt=0, examples=[1000000])]
    method: Annotated[int,Field(default=1, examples=[1])]
    date: Annotated[datetime, Field()]
    payment_id: Annotated[int, Field(examples=[1])]
    status: Annotated[int, Field(default=1, examples=[1])]

class Transaction(TimestampSchema, TransactionBase, UUIDSchema, PersistentDeletion):
    pass

# Returned value.
class TransactionRead(TransactionBase):
    pass

class TransactionReadInternal(TransactionRead):
    transaction_id : int

class TransactionCreate(TransactionBase):
    model_config = ConfigDict(extra="forbid")


class TransactionCreateInternal(TransactionCreate):
    created_at: datetime = Field(default_factory=datetime.now)


class TransactionUpdate(BaseModel):
    amount: Annotated[float, Field(gt=0, examples=[1000000])]
    method: Annotated[int,Field(default=1, examples=[1])]
    payment_id: Annotated[int, Field(examples=[1])]
    status: Annotated[int, Field(default=1, examples=[1])]


class TransactionUpdateInternal(TransactionUpdate):
    updated_at: datetime

class TransactionDelete(TransactionBase):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class TransactionRestoreDeleted(TransactionBase):
    is_deleted: bool
