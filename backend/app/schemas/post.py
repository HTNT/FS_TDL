from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class MediaResponse(BaseModel):
    id: int
    file_url: str
    file_type: str
    file_size: int
    original_filename: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Post(BaseModel):
    id: int
    user_id: str
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    media: List[MediaResponse] = []
    
    class Config:
        from_attributes = True
