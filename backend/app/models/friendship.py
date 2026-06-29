from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class Friendship(Base):
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    low_user = Column(String(12), ForeignKey("users.id"), nullable=False)
    high_user = Column(String(12), ForeignKey("users.id"), nullable=False)
    request_by = Column(String(12), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('low_user', 'high_user', name='unique_friendship'),
    )
