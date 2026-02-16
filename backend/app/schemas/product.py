from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    description: str | None = None
    unit_price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    description: str | None = None
    unit_price: Decimal | None = Field(None, gt=0, decimal_places=2)
    stock: int | None = Field(None, ge=0)
    category_id: int | None = Field(None, gt=0)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    unit_price: Decimal
    stock: int
    category_id: int

    model_config = {"from_attributes": True}
