from pydantic import BaseModel, Field

class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: str | None = Field(None, max_length=100)

class EmployeeUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    position: str | None = Field(None, max_length=100)

class EmployeeRead(BaseModel):
    id: int
    name: str
    position: str | None

    model_config = {
        "from_attributes": True
    }