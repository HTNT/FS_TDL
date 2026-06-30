# 🎯 PROJECT FLOW - TDL (Toàn Bộ Hệ Thống)

## 📊 OVERVIEW - TỔNG QUAN

### Dự án là gì?
**TDL** là một nền tảng **mạng xã hội/diễn đàn** full-stack với:
- Người dùng có thể **đăng ký, đăng nhập**
- Tạo **bài viết (Posts)**
- **Theo dõi (Follow)** người dùng
- **Kết bạn (Friendship)** với người dùng khác

### Tech Stack
| Layer | Tech | Purpose |
|-------|------|---------|
| **Frontend** | React 18 + TypeScript + Tailwind | UI & UX |
| **Backend** | FastAPI + Python 3.11 | API REST |
| **Database** | PostgreSQL | Store data |
| **Cache** | Redis | Session/cache |
| **Auth** | JWT + Bcrypt | Security |
| **DevOps** | Docker + Docker Compose | Deployment |

---

## 🏗️ ARCHITECTURE - KIẾN TRÚC

### Monorepo Structure
```
TDL/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── main.py                  # 🎬 Entry point
│   │   ├── models/                  # 🗄️  Database models (SQLAlchemy)
│   │   │   ├── account.py           # Account table (email, password)
│   │   │   ├── user.py              # User profile (id=yymmddxxxxxx, username)
│   │   │   ├── post.py              # Posts (title, content, user_id)
│   │   │   ├── follow.py            # Follows (follower_id, following_id)
│   │   │   ├── friendship.py        # Friendships (low_user, high_user, status)
│   │   │   └── __init__.py          # ⚠️ MUST import all models here
│   │   ├── schemas/                 # 🔍 Pydantic validators
│   │   │   ├── account.py           # AccountCreate, Account
│   │   │   ├── user.py              # UserCreate, User, UserInDB
│   │   │   ├── post.py              # PostCreate, PostUpdate, Post
│   │   │   ├── follow.py            # FollowCreate, Follow
│   │   │   ├── friendship.py        # Friendship schema
│   │   │   └── __init__.py
│   │   ├── api/v1/                  # 🌐 API endpoints
│   │   │   ├── api.py               # 🔌 Router registration
│   │   │   └── endpoints/
│   │   │       ├── auth.py          # register, login
│   │   │       ├── users.py         # GET users, GET /me
│   │   │       ├── posts.py         # CRUD posts
│   │   │       ├── follows.py       # Follow/unfollow
│   │   │       └── friendships.py   # Friend requests
│   │   ├── core/                    # ⚙️ Config & Security
│   │   │   ├── config.py            # Settings (DATABASE_URL, REDIS_URL, JWT)
│   │   │   ├── security.py          # JWT, bcrypt functions
│   │   │   └── __init__.py
│   │   ├── db/                      # 💾 Database
│   │   │   ├── database.py          # SQLAlchemy engine & session
│   │   │   ├── base.py              # DeclarativeBase for ORM
│   │   │   └── __init__.py
│   │   ├── cache/                   # 🔥 Redis
│   │   │   ├── redis_client.py      # Redis connection
│   │   │   └── __init__.py
│   │   └── utils/                   # 🛠️ Utilities
│   │       ├── id_generator.py      # Generate user ID (yymmddxxxxxx)
│   │       └── __init__.py
│   ├── tests/                       # 🧪 Test files
│   ├── requirements.txt             # Python dependencies
│   ├── pytest.ini                   # Test config
│   └── Dockerfile
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── main.tsx                 # 🎬 Entry point
│   │   ├── App.tsx                  # 📱 Main router & layout
│   │   ├── pages/
│   │   │   ├── Home.tsx             # 🏠 Landing page
│   │   │   ├── Login.tsx            # 🔐 Login form
│   │   │   ├── Register.tsx         # ✍️ Registration form
│   │   │   └── Dashboard.tsx        # 📊 Main page (after login)
│   │   ├── api/
│   │   │   ├── auth.ts              # 🔐 Auth API calls (register, login)
│   │   │   └── users.ts             # 👥 User API calls
│   │   ├── store/
│   │   │   └── authStore.ts         # 🐻 Zustand auth state
│   │   ├── lib/
│   │   │   └── axios.ts             # 📡 Axios config (base URL, interceptors)
│   │   ├── index.css                # 🎨 Tailwind CSS
│   │   └── vite-env.d.ts
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile.dev
│
├── docker-compose.yml               # 🐳 All services
├── docker-compose-with-pgadmin.yml  # 🐳 + PgAdmin
├── PROJECT-FLOW.md                  # 📄 This file
└── README.md
```

---

## 🔄 DATA FLOW - LUỒNG DỮ LIỆU

### 1️⃣ USER REGISTRATION FLOW

```
Client (React)
    ↓
POST /api/v1/auth/register
{email, password, username}
    ↓
auth.py endpoint
    ↓
Check email exists? ❌
Check username exists? ❌
    ↓
Hash password (bcrypt)
    ↓
Create Account in DB
    ↓
db.flush() → Get account.id
    ↓
Generate User ID (yymmddxxxxxx)
    ↓
Create User in DB
    ↓
db.commit()
    ↓
Create JWT token (email as sub)
    ↓
Return {access_token, token_type, user}
    ↓
Frontend
    ├─ Store token in localStorage
    └─ Store user in Zustand
```

### 2️⃣ USER LOGIN FLOW

```
Client (React)
    ↓
POST /api/v1/auth/login
{email, password}
    ↓
auth.py endpoint
    ↓
Find Account by email
    ↓
Verify password (bcrypt)
    ↓
Account is_active? ✓
    ↓
Find User by account_id
    ↓
Create JWT token
    ↓
Return {access_token, token_type, user}
    ↓
Frontend
    ├─ Store token
    └─ Store user
```

### 3️⃣ CREATE POST FLOW

```
Client (React - Dashboard)
    ↓
POST /api/v1/posts/
{title, content} + JWT token
    ↓
posts.py endpoint
    ↓
get_current_user() ← From JWT
    ↓
Validate PostCreate schema
    ├─ title: required
    └─ content: required
    ↓
Create Post in DB
    ├─ user_id = current_user.id
    ├─ title = validated title
    └─ content = validated content
    ↓
Return Post object
    ↓
Frontend updates UI
```

### 4️⃣ FOLLOW USER FLOW

```
Client (React)
    ↓
POST /api/v1/follows/
{following_id} + JWT token
    ↓
follows.py endpoint
    ↓
Check follow not exists
    ↓
Create Follow
    ├─ follower_id = current_user.id
    └─ following_id = target user
    ↓
Return Follow
    ↓
Frontend updates UI
```

### 5️⃣ SEND FRIEND REQUEST FLOW

```
Client (React)
    ↓
POST /api/v1/friendships/
{target_user_id} + JWT token
    ↓
friendships.py endpoint
    ↓
Sort IDs: low_user < high_user
    ↓
Check friendship not exists
    ↓
Create Friendship
    ├─ low_user, high_user (sorted)
    ├─ request_by = current_user.id
    └─ status = "pending"
    ↓
Return Friendship
    ↓
Frontend shows "pending"
```

---

## 📊 DATABASE SCHEMA - CƠ SỬ DỮ LIỆU

### accounts table
```sql
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,                          -- Auto increment
    email VARCHAR UNIQUE NOT NULL,                  -- unique@email.com
    hashed_password VARCHAR NOT NULL,               -- bcrypt hash
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### users table
```sql
CREATE TABLE users (
    id VARCHAR(12) PRIMARY KEY,                     -- yymmddxxxxxx
    account_id INTEGER UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);
```

### posts table
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(12) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### follows table
```sql
CREATE TABLE follows (
    id SERIAL PRIMARY KEY,
    follower_id VARCHAR(12) NOT NULL,
    following_id VARCHAR(12) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(follower_id, following_id),             -- Can't follow twice
    FOREIGN KEY (follower_id) REFERENCES users(id),
    FOREIGN KEY (following_id) REFERENCES users(id)
);
```

### friendships table
```sql
CREATE TABLE friendships (
    id SERIAL PRIMARY KEY,
    low_user VARCHAR(12) NOT NULL,
    high_user VARCHAR(12) NOT NULL,
    request_by VARCHAR(12) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(low_user, high_user),                   -- Can't have duplicate
    FOREIGN KEY (low_user) REFERENCES users(id),
    FOREIGN KEY (high_user) REFERENCES users(id)
);
```

### Relationships (Entity Relationship Diagram)
```
accounts (1) ←──┐
                │ account_id (FK)
                │
users (1) ←──┐  │
             │  │
posts (*)    │  │ (many posts per user)
             │  │
follows (*)  │
             │
friendships (*)

Follow: (1 user) ← follower_id → (many follows)
        (1 user) ← following_id → (many follows)

Friendship: (1 user) ← low_user → (many friendships)
            (1 user) ← high_user → (many friendships)
```

---

## 🔐 AUTHENTICATION FLOW

### JWT Token Generation
```python
# When user registers/logs in
payload = {
    "sub": account.email,           # Subject (unique identifier)
    "exp": datetime + 30 minutes     # Expiration
}
access_token = encode(payload, SECRET_KEY, algorithm="HS256")
```

### JWT Verification
```python
# When user makes request with token
@app.get("/api/v1/users/me")
def get_me(current_user = Depends(get_current_user)):
    # get_current_user decodes JWT token
    # Returns User object if valid
    # Raises 401 if invalid/expired
    return current_user
```

### Password Security
```python
# Registration
plain_password = "user123"
hashed = bcrypt.hash(plain_password)  # Store hashed_password

# Login
provided_password = "user123"
verify_password(provided_password, hashed_password)  # True/False
```

---

## 🌐 API ENDPOINTS

### Authentication
| Method | Endpoint | Request | Response |
|--------|----------|---------|----------|
| POST | `/api/v1/auth/register` | {email, password, username} | {access_token, user} |
| POST | `/api/v1/auth/login` | {email, password} | {access_token, user} |

### Users
| Method | Endpoint | Auth | Response |
|--------|----------|------|----------|
| GET | `/api/v1/users/` | ❌ | List[User] |
| GET | `/api/v1/users/me` | ✅ | User |
| GET | `/api/v1/users/{id}` | ❌ | User |

### Posts
| Method | Endpoint | Auth | Body | Response |
|--------|----------|------|------|----------|
| GET | `/api/v1/posts/` | ❌ | - | List[Post] |
| GET | `/api/v1/posts/{id}` | ❌ | - | Post |
| POST | `/api/v1/posts/` | ✅ | {title, content} | Post |
| PUT | `/api/v1/posts/{id}` | ✅ | {title?, content?} | Post |
| DELETE | `/api/v1/posts/{id}` | ✅ | - | 204 No Content |

### Follows
| Method | Endpoint | Auth | Body | Response |
|--------|----------|------|------|----------|
| GET | `/api/v1/follows/` | ❌ | - | List[Follow] |
| POST | `/api/v1/follows/` | ✅ | {following_id} | Follow |
| DELETE | `/api/v1/follows/{id}` | ✅ | - | 204 No Content |

### Friendships
| Method | Endpoint | Auth | Body | Response |
|--------|----------|------|------|----------|
| GET | `/api/v1/friendships/` | ❌ | - | List[Friendship] |
| POST | `/api/v1/friendships/` | ✅ | {target_user_id} | Friendship |
| PUT | `/api/v1/friendships/{id}` | ✅ | {status} | Friendship |
| DELETE | `/api/v1/friendships/{id}` | ✅ | - | 204 No Content |

---

## 🚀 STARTING THE PROJECT

### Method 1: Docker (Recommended)
```bash
# Windows
RUN.bat

# Or manual
cd TDL
docker-compose up --build
```

Services will start:
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- API Docs: `http://localhost:8000/docs`

### Method 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Method 3: Database Setup
```bash
# View database
docker exec -it postgres_db psql -U postgres -d app_db

# Or use PgAdmin
docker-compose -f docker-compose-with-pgadmin.yml up
# PgAdmin: http://localhost:5050
```

---

## 🔄 5-STEP ADDING NEW FEATURE

### Example: Adding "Comments" Feature

**Step 1: Create Model**
```python
# backend/app/models/comment.py
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(String(12), ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
```

**Step 2: Import Model**
```python
# backend/app/models/__init__.py
from app.models.comment import Comment  # Add this
```

**Step 3: Create Schema**
```python
# backend/app/schemas/comment.py
class CommentCreate(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    post_id: int
    user_id: str
    content: str
    
    class Config:
        from_attributes = True
```

**Step 4: Create Endpoints**
```python
# backend/app/api/v1/endpoints/comments.py
@router.post("/posts/{post_id}/comments")
def create_comment(post_id: int, comment: CommentCreate, 
                  current_user = Depends(get_current_user)):
    db_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    return db_comment
```

**Step 5: Register Router**
```python
# backend/app/api/v1/api.py
from app.api.v1.endpoints import comments
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
```

---

## 🧪 TESTING

### Backend Tests
```bash
cd backend
pytest                      # Run all tests
pytest tests/test_main.py   # Run specific file
pytest -v                   # Verbose
pytest --cov               # With coverage
```

### Frontend Linting
```bash
cd frontend
npm run lint        # Check lint errors
npm run build       # Build & type check
```

---

## ⚙️ ENVIRONMENT VARIABLES

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🐛 DEBUGGING

### Backend Issues
```bash
# Check uvicorn logs
docker logs fastapi_backend

# Run locally for better debugging
cd backend
uvicorn app.main:app --reload --log-level debug

# Check database
docker exec -it postgres_db psql -U postgres -d app_db
\dt              # List all tables
SELECT * FROM users;
```

### Frontend Issues
```bash
# Check browser console
# Vite HMR should work automatically
# Check network tab for API calls
# Check Zustand store: authStore
```

### Docker Issues
```bash
# View all containers
docker ps -a

# View logs
docker logs container_name

# Restart services
docker-compose restart

# Full rebuild
docker-compose down
docker-compose up --build
```

---

## 📝 CODE CONVENTIONS

### Backend
- Models: Singular (User, Post, Follow)
- Endpoints: Use FastAPI decorators (@router.get, @router.post)
- Error handling: HTTPException with status codes
- Database: Use Session dependency injection

### Frontend
- Components: PascalCase (Home, Login)
- Store: Zustand with clear actions
- API: Separate client files in api/ folder
- Styling: Tailwind CSS classes

---

## 🔗 QUICK LINKS

| Item | Path |
|------|------|
| Main Backend Entry | `backend/app/main.py` |
| Main Frontend Entry | `frontend/src/App.tsx` |
| Auth Logic | `backend/app/core/security.py` |
| API Router | `backend/app/api/v1/api.py` |
| Database Config | `backend/app/core/config.py` |
| API Docs | http://localhost:8000/docs |
| Swagger UI | http://localhost:8000/redoc |

---

## 🎓 LEARNING PATH

1. **Understand Database**: Check `PROJECT-FLOW.md` → Database Schema section
2. **Understand Authentication**: Check auth.py endpoint + security.py
3. **Understand CRUD**: Check any endpoints/ file (e.g., posts.py)
4. **Add New Feature**: Follow 5-Step process above
5. **Test**: Use API Docs at http://localhost:8000/docs

---

**Last Updated**: June 2026
**Status**: 🟢 Development Ready
