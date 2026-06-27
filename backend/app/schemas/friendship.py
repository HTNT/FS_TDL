from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FriendshipCreate(BaseModel):
    user_id_2: int

class Friendship(BaseModel):
    id: int
    user_id_1: int
    user_id_2: int
    created_at: datetime
    
    class Config:
        from_attributes = True
