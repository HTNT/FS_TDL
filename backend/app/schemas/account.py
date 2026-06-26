from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AccountCreate(BaseModel):
    email: EmailStr
    password: str

class AccountInDB(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Account(AccountInDB):
    pass
