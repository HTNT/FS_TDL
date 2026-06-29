from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FollowCreate(BaseModel):
    following_id: str

class Follow(BaseModel):
    id: int
    follower_id: str
    following_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
