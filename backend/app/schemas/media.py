from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

class MediaCreate(BaseModel):
    file_type: MediaType
    file_size: int
    original_filename: str

class Media(BaseModel):
    id: int
    post_id: int
    file_url: str
    file_type: MediaType
    file_size: int
    original_filename: str
    created_at: datetime
    
    class Config:
        from_attributes = True
