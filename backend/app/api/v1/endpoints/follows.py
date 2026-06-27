from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.follow import Follow
from app.models.user import User
from app.schemas.follow import Follow as FollowSchema, FollowCreate
from app.utils import generate_user_id

router = APIRouter()

@router.post("/", response_model=FollowSchema, status_code=status.HTTP_201_CREATED)
def follow_user(follower_id: str, follow_in: FollowCreate, db: Session = Depends(get_db)):
    """Follow user"""
    following_id = follow_in.following_id
    
    # Check if both users exist
    follower = db.query(User).filter(User.id == follower_id).first()
    following = db.query(User).filter(User.id == following_id).first()
    
    if not follower or not following:
        raise HTTPException(status_code=404, detail="User not found")
    
    if follower_id == following_id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")
    
    # Check if already following
    existing = db.query(Follow).filter(
        (Follow.follower_id == follower_id) & (Follow.following_id == following_id)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already following")
    
    follow = Follow(id=generate_user_id(), follower_id=follower_id, following_id=following_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

@router.get("/followers/{user_id}", response_model=List[FollowSchema])
def get_followers(user_id: str, db: Session = Depends(get_db)):
    """Get followers of user"""
    followers = db.query(Follow).filter(Follow.following_id == user_id).all()
    return followers

@router.get("/following/{user_id}", response_model=List[FollowSchema])
def get_following(user_id: str, db: Session = Depends(get_db)):
    """Get users that user is following"""
    following = db.query(Follow).filter(Follow.follower_id == user_id).all()
    return following

@router.delete("/{follow_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(follow_id: str, db: Session = Depends(get_db)):
    """Unfollow user"""
    follow = db.query(Follow).filter(Follow.id == follow_id).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Follow not found")
    
    db.delete(follow)
    db.commit()
    return None
