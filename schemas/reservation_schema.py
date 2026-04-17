from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class ReservationCreate(BaseModel):
    table_id: int
    start_time: datetime
    end_time: datetime
    
    @validator('end_time')
    def validate_end_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v
    
    @validator('start_time')
    def validate_start_time(cls, v):
        if v < datetime.now():
            raise ValueError('start_time cannot be in the past')
        return v

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    table_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True