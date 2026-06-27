from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Post(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
