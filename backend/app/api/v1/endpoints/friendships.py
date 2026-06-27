from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.friendship import Friendship
from app.models.user import User
from app.schemas.friendship import Friendship as FriendshipSchema, FriendshipCreate
from app.utils import generate_user_id

router = APIRouter()

@router.post("/", response_model=FriendshipSchema, status_code=status.HTTP_201_CREATED)
def add_friend(user_id: str, friend_in: FriendshipCreate, db: Session = Depends(get_db)):
    """Add friend"""
    user_id_2 = friend_in.user_id_2
    
    # Check if both users exist
    user1 = db.query(User).filter(User.id == user_id).first()
    user2 = db.query(User).filter(User.id == user_id_2).first()
    
    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_id == user_id_2:
        raise HTTPException(status_code=400, detail="Cannot add yourself as friend")
    
    # Check if friendship already exists
    existing = db.query(Friendship).filter(
        ((Friendship.user_id_1 == user_id) & (Friendship.user_id_2 == user_id_2)) |
        ((Friendship.user_id_1 == user_id_2) & (Friendship.user_id_2 == user_id))
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already friends")
    
    # Ensure user_id_1 < user_id_2 for consistency (string comparison)
    if user_id > user_id_2:
        user_id, user_id_2 = user_id_2, user_id
    
    friendship = Friendship(id=generate_user_id(), user_id_1=user_id, user_id_2=user_id_2)
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship

@router.get("/", response_model=List[FriendshipSchema])
def get_friends(user_id: str, db: Session = Depends(get_db)):
    """Get all friends of user"""
    friendships = db.query(Friendship).filter(
        (Friendship.user_id_1 == user_id) | (Friendship.user_id_2 == user_id)
    ).all()
    return friendships

@router.delete("/{friendship_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_friend(friendship_id: str, db: Session = Depends(get_db)):
    """Remove friend"""
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    
    db.delete(friendship)
    db.commit()
    return None
