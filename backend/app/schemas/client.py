from pydantic import BaseModel, EmailStr, Field

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(None, max_length=30)
    address: str | None = None

class ClientUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=30)
    address: str | None = None

class ClientRead(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    address: str | None

    model_config = {
        "from_attributes": True
    }