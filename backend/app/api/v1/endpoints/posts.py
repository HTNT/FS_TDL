from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.post import Post
from app.models.user import User
from app.schemas.post import Post as PostSchema, PostCreate, PostUpdate
from app.utils import generate_user_id

router = APIRouter()

@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(post_in: PostCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create new post"""
    db_post = Post(
        id=generate_user_id(),
        user_id=current_user.id,
        title=post_in.title,
        content=post_in.content
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostSchema])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all posts"""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostSchema)
def get_post(post_id: str, db: Session = Depends(get_db)):
    """Get post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostSchema)
def update_post(post_id: str, post_in: PostUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for field, value in post_in.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(post)
    db.commit()
    return None
