# 🎯 HỆ THỐNG BACKEND - FLOW TẠO ĐỐI TƯỢNG MỚI

## THỨ TỰ TẠO: 5 BƯỚC

| Bước | File | Làm gì | Lý do | Ví dụ |
|------|------|--------|-------|-------|
| **1** | `app/models/post.py` | Tạo class với `Column()` | Define database schema | `class Post(Base): id, title, content, user_id...` |
| **2** | `app/models/__init__.py` | Thêm `from app.models.post import Post` | Import model cho `Base.metadata.create_all()` | Bảng tự động tạo |
| **3** | `app/schemas/post.py` | Tạo `PostCreate`, `Post` Pydantic | Validate input, serialize output | `class PostCreate(name: str)` |
| **4** | `app/api/v1/endpoints/posts.py` | Viết `@router.get/post/put/delete()` | Tạo REST API endpoints | `@router.post("/")` |
| **5** | `app/api/v1/api.py` | `import posts` + `include_router()` | Đăng ký endpoints vào API | `/api/v1/posts/` ready |

---

## VÌ SAO THỨ TỰ ĐÓ?

```
1. Model trước → Define cấu trúc
   ↓
2. Import model → ORM tìm được
   ↓
3. Schema → Validate dữ liệu
   ↓
4. Endpoint → API handle request
   ↓
5. Router → Đăng ký endpoint
```

**Nếu làm sai thứ tự:**
- ❌ Không import model → Table không tạo
- ❌ Endpoint trước schema → Không validate
- ❌ Quên router → Endpoint không được gọi

---

## CHI TIẾT TỪNG BƯỚC

### **Bước 1: Model** (LÝ DO: Map class Python → Database table)

**File:** `app/models/post.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

**Giải thích:**
- `__tablename__` = Tên bảng trong database
- `Column()` = Định nghĩa cột (type, constraints, default)
- `ForeignKey()` = Liên kết với bảng users
- `server_default=func.now()` = Tự động set thời gian

---

### **Bước 2: Import Model** (LÝ DO: `Base.metadata` cần biết class này)

**File:** `app/models/__init__.py`

```python
from app.models.user import User
from app.models.post import Post  # ← Thêm dòng này
```

**Tại sao cần?**

Trong `app/main.py` có:
```python
Base.metadata.create_all(bind=engine)
```

Nó sẽ scan tất cả models từ `Base` → Tìm Post class → CREATE TABLE posts

Nếu không import → Post class không được load → Table không tạo!

---

### **Bước 3: Schema** (LÝ DO: Validate input, không nhận data bừa bộ)

**File:** `app/schemas/post.py`

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Input từ client (có validate)
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)

# Có thể cập nhật (fields optional)
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Output trả về client
class Post(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Map SQLAlchemy object → Pydantic
```

**Giải thích:**
- `PostCreate` = Data nhận từ client (bắt buộc có title, content)
- `PostUpdate` = Optional fields (có thể không có)
- `Post` = Data trả về client (không có password, thông tin nhạy cảm)
- `Field(..., min_length=1)` = Validate (không được rỗng)
- `from_attributes = True` = Cho phép map từ ORM objects

---

### **Bước 4: Endpoint** (LÝ DO: Client gọi API, backend handle request)

**File:** `app/api/v1/endpoints/posts.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.post import Post
from app.schemas.post import Post as PostSchema, PostCreate, PostUpdate

router = APIRouter()

# GET - Lấy danh sách posts
@router.get("/", response_model=List[PostSchema])
def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách bài viết"""
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

# GET - Lấy post theo ID
@router.get("/{post_id}", response_model=PostSchema)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 bài viết"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# POST - Tạo post mới
@router.post("/", response_model=PostSchema, status_code=status.HTTP_201_CREATED)
def create_post(post_in: PostCreate, db: Session = Depends(get_db)):
    """Tạo bài viết mới"""
    db_post = Post(
        title=post_in.title,
        content=post_in.content,
        user_id=1  # TODO: Lấy từ current_user
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# PUT - Cập nhật post
@router.put("/{post_id}", response_model=PostSchema)
def update_post(post_id: int, post_in: PostUpdate, db: Session = Depends(get_db)):
    """Cập nhật bài viết"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    for field, value in post_in.dict(exclude_unset=True).items():
        setattr(post, field, value)
    
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# DELETE - Xóa post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Xóa bài viết"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return None
```

**Các endpoints tạo ra:**
- `GET /posts/` → Danh sách posts
- `GET /posts/{id}` → Chi tiết 1 post
- `POST /posts/` → Tạo post mới
- `PUT /posts/{id}` → Cập nhật post
- `DELETE /posts/{id}` → Xóa post

---

### **Bước 5: Router** (LÝ DO: `/api/v1/posts/` chưa được đăng ký)

**File:** `app/api/v1/api.py`

```python
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, posts  # ← Thêm import

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])  # ← Thêm dòng này
```

**Kết quả:**
- `/api/v1/posts/` ← Endpoints ready!
- `/api/v1/posts/{id}`
- `/api/v1/posts/` (POST)

---

## CHECKLIST

- [ ] Tạo `app/models/post.py`
- [ ] Thêm import vào `app/models/__init__.py`
- [ ] Tạo `app/schemas/post.py`
- [ ] Tạo `app/api/v1/endpoints/posts.py`
- [ ] Update `app/api/v1/api.py` (import + include_router)
- [ ] Docker restart (hoặc table auto-create)
- [ ] Test endpoints: http://localhost:8000/docs

---

## TEST ENDPOINTS

### Cách 1: API Docs (Khuyến nghị)
1. Mở: http://localhost:8000/docs
2. Scroll tìm "posts" section
3. Click "Try it out" → Test

### Cách 2: cURL
```bash
# Lấy danh sách
curl http://localhost:8000/api/v1/posts/

# Tạo post mới
curl -X POST "http://localhost:8000/api/v1/posts/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "content": "World"}'

# Lấy chi tiết
curl http://localhost:8000/api/v1/posts/1

# Cập nhật
curl -X PUT "http://localhost:8000/api/v1/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated"}'

# Xóa
curl -X DELETE http://localhost:8000/api/v1/posts/1
```

---

## FLOW TỔNG QUÁT

```
Client Request
    ↓
POST /api/v1/posts/
    ↓
app/api/v1/api.py
    ↓ (router.include_router)
app/api/v1/endpoints/posts.py
    ↓ (@router.post("/"))
create_post(post_in: PostCreate)
    ↓
Pydantic validate (schemas/post.py)
    ↓ (PostCreate schema)
Valid? ✓
    ↓
SQLAlchemy ORM (models/post.py)
    ↓ (Create Post instance)
Database
    ↓ (INSERT INTO posts)
PostgreSQL
    ↓
Return PostSchema
    ↓
Client Response (201 Created + JSON)
```

---

## SUMMARY

| | Mục đích |
|---|----------|
| **Model** | Map class → Database table |
| **Import** | Load class để ORM tìm được |
| **Schema** | Validate input, serialize output |
| **Endpoint** | Handle request (GET/POST/PUT/DELETE) |
| **Router** | Đăng ký endpoint vào API |

**Mỗi lần thêm object mới, cứ repeat 5 bước này!** 🔄
