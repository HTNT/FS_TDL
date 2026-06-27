from sqlalchemy import Column, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

class Friendship(Base):
    __tablename__ = "friendships"
    
    id = Column(String(12), primary_key=True, index=True)
    user_id_1 = Column(String(12), ForeignKey("users.id"), nullable=False)
    user_id_2 = Column(String(12), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id_1', 'user_id_2', name='unique_friendship'),
    )
