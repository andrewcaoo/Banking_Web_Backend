from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class Order(BaseModel):
    amount: Annotated[float, Field(gt=0, examples=[5000000])]
    bank_code: Annotated[str, Field(examples=[""])]
    order_description: Annotated[str, Field(examples=[""])]
    order_type: Annotated[str, Field(examples=['topup'])]
    language: Annotated[str, Field(examples=['vi'])]
    payment_id: Annotated[int, Field(examples=[1])]