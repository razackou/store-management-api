from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class OrderProductCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    client_id: int = Field(..., gt=0)
    employee_id: int | None = Field(None, gt=0)
    status: str = Field(..., min_length=1, max_length=50)
    products: list[OrderProductCreate] = Field(..., min_length=1)


class OrderRead(BaseModel):
    id: int
    order_date: datetime
    total_amount: Decimal
    status: str
    client_id: int
    employee_id: int | None = None

    model_config = {"from_attributes": True}
