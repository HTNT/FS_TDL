from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FollowCreate(BaseModel):
    following_id: int

class Follow(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
