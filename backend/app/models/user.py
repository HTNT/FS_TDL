from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(12), primary_key=True, index=True)  # yymmddxxxxxx
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, unique=True)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
