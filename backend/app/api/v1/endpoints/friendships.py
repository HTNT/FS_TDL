from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.friendship import Friendship
from app.models.user import User
from app.schemas.friendship import Friendship as FriendshipSchema, FriendshipCreate, FriendshipUpdate

router = APIRouter()

@router.post("/", response_model=FriendshipSchema, status_code=status.HTTP_201_CREATED)
def send_friend_request(friend_in: FriendshipCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Send friend request"""
    requester = current_user.id
    recipient = friend_in.high_user
    
    # Check if recipient exists
    user_recipient = db.query(User).filter(User.id == recipient).first()
    if not user_recipient:
        raise HTTPException(status_code=404, detail="User not found")
    
    if requester == recipient:
        raise HTTPException(status_code=400, detail="Cannot add yourself as friend")
    
    # Determine low_user and high_user (sorted)
    low_user = min(requester, recipient)
    high_user = max(requester, recipient)
    
    # Check if request already exists
    existing = db.query(Friendship).filter(
        (Friendship.low_user == low_user) & (Friendship.high_user == high_user)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Friendship request already exists")
    
    friendship = Friendship(
        low_user=low_user,
        high_user=high_user,
        request_by=requester,
        status="pending"
    )
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship

@router.get("/", response_model=List[FriendshipSchema])
def get_friendships(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all friendships of current user"""
    friendships = db.query(Friendship).filter(
        (Friendship.low_user == current_user.id) | (Friendship.high_user == current_user.id)
    ).all()
    return friendships

@router.put("/{friendship_id}", response_model=FriendshipSchema)
def update_friendship_status(friendship_id: int, update_in: FriendshipUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Accept or reject friend request"""
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    
    # Only the recipient (not requester) can respond
    if current_user.id == friendship.request_by:
        raise HTTPException(status_code=403, detail="Only recipient can respond")
    
    friendship.status = update_in.status
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship

@router.delete("/{friendship_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_friend(friendship_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Remove friend"""
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    
    # Only low_user or high_user can remove
    if current_user.id not in [friendship.low_user, friendship.high_user]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(friendship)
    db.commit()
    return None
