from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import FileResponse
import os

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.post import Post
from app.models.media import Media
from app.models.user import User
from app.schemas.post import Post as PostSchema, PostCreate, PostUpdate
from app.utils.file_handler import save_upload_file, delete_file, get_file_url

router = APIRouter()

@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def create_post(
    title: str = Form(..., min_length=1, max_length=255),
    content: str = Form(..., min_length=1),
    files: Optional[List[UploadFile]] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new post with optional media files (images/videos)"""
    
    # Tạo bài viết mới
    db_post = Post(
        user_id=current_user.id,
        title=title,
        content=content
    )
    db.add(db_post)
    db.flush()  # Lấy ID mới tạo
    
    # Xử lý upload file nếu có
    if files:
        for file in files:
            if file and file.filename:
                try:
                    file_path, media_type, file_size = await save_upload_file(file, db_post.id)
                    file_url = get_file_url(file_path)
                    
                    # Tạo record media
                    media = Media(
                        post_id=db_post.id,
                        file_url=file_url,
                        file_type=media_type,
                        file_size=file_size,
                        original_filename=file.filename
                    )
                    db.add(media)
                except HTTPException:
                    # Xóa bài viết nếu có lỗi upload
                    db.rollback()
                    raise
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=List[PostSchema])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all posts"""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Get post by ID"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostSchema)
def update_post(post_id: int, post_in: PostUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
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
def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete post and associated media files"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Xóa các file media liên quan
    for media in post.media:
        delete_file(media.file_url.replace("/files/", ""))
    
    db.delete(post)
    db.commit()
    return None

@router.get("/files/{file_path:path}")
def get_file(file_path: str):
    """Download media file"""
    full_path = os.path.join("uploads", file_path)
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Bảo vệ lấy file: chỉ cho phép trong thư mục uploads
    if not os.path.abspath(full_path).startswith(os.path.abspath("uploads")):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return FileResponse(path=full_path)

@router.post("/{post_id}/media", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
async def add_media_to_post(
    post_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add media files to existing post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Upload files
    for file in files:
        if file and file.filename:
            try:
                file_path, media_type, file_size = await save_upload_file(file, post.id)
                file_url = get_file_url(file_path)
                
                media = Media(
                    post_id=post.id,
                    file_url=file_url,
                    file_type=media_type,
                    file_size=file_size,
                    original_filename=file.filename
                )
                db.add(media)
            except HTTPException:
                db.rollback()
                raise
    
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_media(
    post_id: int,
    media_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete specific media file from post"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    media = db.query(Media).filter(Media.id == media_id, Media.post_id == post_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media file not found")
    
    # Xóa file vật lý
    delete_file(media.file_url.replace("/files/", ""))
    
    # Xóa record database
    db.delete(media)
    db.commit()
    return None
