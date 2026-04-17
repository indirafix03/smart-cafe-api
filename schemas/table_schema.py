from pydantic import BaseModel, Field

class TableCreate(BaseModel):
    table_number: int = Field(..., ge=1)
    capacity: int = Field(..., ge=1, le=20)

class TableResponse(BaseModel):
    id: int
    table_number: int
    capacity: int
    is_available: bool
    
    class Config:
        from_attributes = True