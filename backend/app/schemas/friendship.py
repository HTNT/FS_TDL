from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Friendship(BaseModel):
    id: int
    low_user: str
    high_user: str
    request_by: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
