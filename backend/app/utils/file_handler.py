import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException, status
from app.models.media import MediaType

# Config
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/mpeg", "video/quicktime", "video/x-msvideo"}
ALLOWED_TYPES = ALLOWED_IMAGE_TYPES | ALLOWED_VIDEO_TYPES

def ensure_upload_dir():
    """Đảm bảo thư mục uploads tồn tại"""
    Path(UPLOAD_DIR).mkdir(exist_ok=True)

async def save_upload_file(file: UploadFile, post_id: int) -> tuple[str, MediaType, int]:
    """
    Lưu file được upload và trả về (file_path, media_type, file_size)
    
    Args:
        file: File được upload
        post_id: ID của bài viết
        
    Returns:
        Tuple: (file_path, media_type, file_size)
        
    Raises:
        HTTPException: Nếu file không hợp lệ
    """
    ensure_upload_dir()
    
    # Kiểm tra MIME type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {ALLOWED_TYPES}"
        )
    
    # Xác định media type
    if file.content_type in ALLOWED_IMAGE_TYPES:
        media_type = MediaType.IMAGE
        subfolder = "images"
    else:
        media_type = MediaType.VIDEO
        subfolder = "videos"
    
    # Đọc file content
    content = await file.read()
    file_size = len(content)
    
    # Kiểm tra kích thước file
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Tạo tên file duy nhất
    file_extension = Path(file.filename).suffix
    unique_filename = f"{post_id}_{uuid.uuid4()}{file_extension}"
    
    # Tạo đường dẫn lưu file
    upload_subdir = os.path.join(UPLOAD_DIR, subfolder)
    Path(upload_subdir).mkdir(exist_ok=True, parents=True)
    
    file_path = os.path.join(upload_subdir, unique_filename)
    
    # Lưu file
    with open(file_path, "wb") as f:
        f.write(content)
    
    return file_path, media_type, file_size

def delete_file(file_path: str):
    """Xóa file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")

def get_file_url(file_path: str) -> str:
    """Chuyển đổi đường dẫn file thành URL"""
    return f"/files/{file_path.replace(os.sep, '/')}"
