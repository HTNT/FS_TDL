# 📖 GIẢI THÍCH LUỒNG TOÀN BỘ HỆ THỐNG

## 🏗️ KIẾN TRÚC TỔNG QUAN

```
┌─────────────┐      HTTP Request       ┌──────────────┐
│   Browser   │ ──────────────────────> │   Frontend   │
│ (localhost: │                          │   (React)    │
│    5173)    │ <────────────────────── │  Port 5173   │
└─────────────┘      HTML/CSS/JS        └──────────────┘
                                                │
                                                │ API Call
                                                │ (Axios)
                                                ▼
                                         ┌──────────────┐
                                         │   Backend    │
                                         │  (FastAPI)   │
                                         │  Port 8000   │
                                         └──────────────┘
                                                │
                        ┌───────────────────────┼───────────────────────┐
                        │                       │                       │
                        ▼                       ▼                       ▼
                 ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
                 │ PostgreSQL  │        │    Redis    │        │     JWT     │
                 │  Database   │        │    Cache    │        │    Auth     │
                 │  Port 5432  │        │  Port 6379  │        │  Security   │
                 └─────────────┘        └─────────────┘        └─────────────┘
```

---

## 🔄 LUỒNG 1: ĐĂNG KÝ USER (REGISTER)

### Bước 1: User nhập thông tin trên giao diện
```
File: frontend/src/pages/Register.tsx
```
- User điền: email, username, password, confirm password
- React Hook Form validate dữ liệu
- Submit form

### Bước 2: Frontend gửi API request
```typescript
// File: frontend/src/api/auth.ts
authApi.register({
  email: "test@example.com",
  username: "testuser",
  password: "123456"
})
```
- Axios gửi POST request đến: `http://localhost:8000/api/v1/auth/register`
- Headers: `Content-Type: application/json`

### Bước 3: Backend nhận request
```python
# File: backend/app/api/v1/endpoints/auth.py
@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
```
- FastAPI nhận data
- Pydantic validate schema (UserCreate)
- Kiểm tra email/username đã tồn tại chưa

### Bước 4: Mã hóa mật khẩu
```python
# File: backend/app/core/security.py
hashed_password = get_password_hash(user_in.password)
# Dùng Bcrypt để hash: "123456" -> "$2b$12$..."
```

### Bước 5: Lưu vào Database
```python
# File: backend/app/api/v1/endpoints/auth.py
db_user = User(
    email=user_in.email,
    username=user_in.username,
    hashed_password=hashed_password
)
db.add(db_user)
db.commit()
```
- SQLAlchemy insert vào PostgreSQL
- Bảng: `users`

### Bước 6: Trả về response
```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2026-06-12T..."
}
```

### Bước 7: Frontend xử lý response
```typescript
// File: frontend/src/pages/Register.tsx
onSuccess: () => {
  alert('Registration successful! Please login.')
  navigate('/login')
}
```
- Hiển thị thông báo thành công
- Chuyển hướng đến trang login

---

## 🔄 LUỒNG 2: ĐĂNG NHẬP (LOGIN)

### Bước 1: User nhập email & password
```
File: frontend/src/pages/Login.tsx
```

### Bước 2: Frontend gửi login request
```typescript
// File: frontend/src/api/auth.ts
authApi.login({
  username: "test@example.com",  // OAuth2 dùng "username" field
  password: "123456"
})
```
- Gửi dạng FormData (OAuth2 standard)
- POST đến: `http://localhost:8000/api/v1/auth/login`

### Bước 3: Backend xác thực
```python
# File: backend/app/api/v1/endpoints/auth.py
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm, db: Session):
```

#### 3a. Tìm user trong database
```python
user = db.query(User).filter(User.email == form_data.username).first()
```

#### 3b. Verify password
```python
# File: backend/app/core/security.py
verify_password(form_data.password, user.hashed_password)
# So sánh: "123456" với hash "$2b$12$..."
```

#### 3c. Tạo JWT token
```python
# File: backend/app/core/security.py
access_token = create_access_token(
    data={"sub": user.email},
    expires_delta=timedelta(minutes=30)
)
# JWT: "eyJhbGciOiJIUzI1NiIs..."
```

### Bước 4: Trả về token
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Bước 5: Frontend lưu token
```typescript
// File: frontend/src/store/authStore.ts (Zustand)
setAuth(user, token) {
  localStorage.setItem('access_token', token)
  set({ user, token, isAuthenticated: true })
}
```
- Lưu vào localStorage
- Cập nhật Zustand store

### Bước 6: Chuyển đến Dashboard
```typescript
navigate('/dashboard')
```

---

## 🔄 LUỒNG 3: XEM DANH SÁCH USERS (DASHBOARD)

### Bước 1: Component mount
```
File: frontend/src/pages/Dashboard.tsx
```

### Bước 2: TanStack Query fetch data
```typescript
const { data: users } = useQuery({
  queryKey: ['users'],
  queryFn: usersApi.getUsers,
  enabled: isAuthenticated
})
```

### Bước 3: Axios gửi request với token
```typescript
// File: frontend/src/lib/axios.ts
// Interceptor tự động thêm token
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  config.headers.Authorization = `Bearer ${token}`
  return config
})
```
- GET đến: `http://localhost:8000/api/v1/users/`
- Header: `Authorization: Bearer eyJhbGci...`

### Bước 4: Backend verify token
```python
# File: backend/app/api/v1/endpoints/auth.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
```
- JWT decode token
- Kiểm tra expiration time
- Xác thực user

### Bước 5: Query database
```python
# File: backend/app/api/v1/endpoints/users.py
@router.get("/")
def get_users(skip: int = 0, limit: int = 100, db: Session):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
```
- SQLAlchemy SELECT * FROM users LIMIT 100

### Bước 6: Trả về danh sách
```json
[
  {
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "is_active": true,
    ...
  }
]
```

### Bước 7: Frontend hiển thị trong table
```tsx
{users?.map((user) => (
  <tr key={user.id}>
    <td>{user.id}</td>
    <td>{user.username}</td>
    <td>{user.email}</td>
    ...
  </tr>
))}
```

---

## 🔄 LUỒNG 4: ĐĂNG XUẤT (LOGOUT)

### Bước 1: User click button Logout
```typescript
// File: frontend/src/pages/Dashboard.tsx
const handleLogout = () => {
  logout()
  navigate('/login')
}
```

### Bước 2: Xóa token khỏi store
```typescript
// File: frontend/src/store/authStore.ts
logout: () => {
  localStorage.removeItem('access_token')
  set({ user: null, token: null, isAuthenticated: false })
}
```

### Bước 3: Chuyển về trang login
```typescript
navigate('/login')
```

---

## 🔐 BẢO MẬT & AUTHENTICATION

### 1. Password Security
```
Plain password: "123456"
        ↓
Bcrypt hash: "$2b$12$K8X5..."
        ↓
Stored in database (KHÔNG lưu plain text)
```

### 2. JWT Token Structure
```
Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"sub": "test@example.com", "exp": 1234567890}
Signature: HMACSHA256(header + payload, SECRET_KEY)
        ↓
Token: "eyJhbGci...IUzI1NiIs.eyJzdWI...iOiJ0ZXN0.SflKx...wRJSMeKKF2Q"
```

### 3. Request Authorization Flow
```
1. User login → Nhận JWT token
2. Lưu token vào localStorage
3. Mỗi API request → Gửi kèm: Authorization: Bearer <token>
4. Backend verify token → Cho phép/Từ chối
```

---

## 🗄️ DATABASE SCHEMA

### Bảng: users
```sql
CREATE TABLE users (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR UNIQUE NOT NULL,
    username        VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    is_superuser    BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP
);
```

---

## 🚀 DOCKER SERVICES

### 1. PostgreSQL (postgres_db)
- Port: 5432
- Lưu trữ: users, sessions, data
- Volume: postgres_data (persistent)

### 2. Redis (redis_cache)
- Port: 6379
- Cache data, sessions
- Volume: redis_data

### 3. Backend (fastapi_backend)
- Port: 8000
- FastAPI + Uvicorn
- Auto-reload khi code thay đổi

### 4. Frontend (react_frontend)
- Port: 5173
- Vite dev server
- Hot Module Replacement (HMR)

---

## 📦 THƯ VIỆN & CÔNG DỤNG

### Frontend:
- **React Router**: Điều hướng trang (/, /login, /register, /dashboard)
- **Axios**: HTTP client, gọi API
- **TanStack Query**: Cache & quản lý API state
- **React Hook Form**: Validate & quản lý form
- **Zustand**: Global state (auth, user)
- **Tailwind CSS**: Styling

### Backend:
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **Pydantic**: Data validation
- **JWT**: Token authentication
- **Bcrypt**: Password hashing
- **Redis**: Caching
- **Pytest**: Testing

---

## 🔄 TỔNG KẾT FLOW HOÀN CHỈNH

```
User Action (Browser)
        ↓
React Component (UI)
        ↓
React Hook Form (Validation)
        ↓
Zustand Store (State Management)
        ↓
Axios (HTTP Client)
        ↓
TanStack Query (API Cache)
        ↓
API Request → Backend (FastAPI)
        ↓
Pydantic (Schema Validation)
        ↓
Security (JWT/Bcrypt)
        ↓
SQLAlchemy (ORM)
        ↓
PostgreSQL (Database)
        ↓
Response → Frontend
        ↓
TanStack Query (Cache)
        ↓
React Component (Re-render)
        ↓
User sees result
```

---

## 💡 CÁC KHÁI NIỆM QUAN TRỌNG

### 1. SSR vs CSR
- **CSR** (Client Side Rendering): React render ở browser
- App này dùng CSR với React

### 2. REST API
- **GET** /users → Lấy danh sách
- **POST** /auth/register → Tạo mới
- **POST** /auth/login → Xác thực

### 3. State Management
- **Local State**: useState trong component
- **Global State**: Zustand (auth, user)
- **Server State**: TanStack Query (API data)

### 4. Middleware
- **Axios Interceptor**: Thêm token vào mọi request
- **CORS**: Cho phép frontend:5173 gọi backend:8000

---

Hy vọng giải thích này giúp bạn hiểu rõ toàn bộ luồng hoạt động! 🚀
