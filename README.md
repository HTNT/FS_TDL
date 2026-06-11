# 🚀 Full-Stack Monorepo - React + FastAPI

Dự án full-stack với Frontend (React + TypeScript) và Backend (FastAPI + Python) trong cùng một repository.

## 📸 Demo

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🛠️ Tech Stack

### Frontend
- ⚛️ **React 18** - UI Library
- 🔷 **TypeScript** - Type Safety
- 🎨 **Tailwind CSS** - Styling
- 🔄 **React Router** - Navigation
- 📡 **Axios** - HTTP Client
- 🔥 **TanStack Query** - Server State Management
- 📝 **React Hook Form** - Form Management
- 🐻 **Zustand** - Global State Management
- ⚡ **Vite** - Build Tool

### Backend
- 🚀 **FastAPI** - Web Framework
- 🐍 **Python 3.11** - Language
- 🔥 **Uvicorn** - ASGI Server
- 🗃️ **PostgreSQL** - Database
- 💾 **Redis** - Cache
- 🔐 **JWT** - Authentication
- 🔒 **Bcrypt** - Password Hashing
- 📊 **SQLAlchemy** - ORM
- ✅ **Pydantic** - Data Validation
- 🧪 **Pytest** - Testing
- 🐳 **Docker** - Containerization

## 🚀 Quick Start

### Với Docker (Khuyến nghị)

```bash
# Clone repository
git clone <repo-url>
cd TDL

# Khởi động tất cả services
docker-compose up --build
```

Hoặc click đúp file **`RUN.bat`** (Windows)

### Chạy Local

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📁 Cấu trúc dự án

```
📦 TDL/
├── 📁 backend/              # FastAPI Backend
│   ├── 📁 app/
│   │   ├── 📁 api/          # API endpoints
│   │   ├── 📁 core/         # Config & Security
│   │   ├── 📁 db/           # Database
│   │   ├── 📁 models/       # SQLAlchemy models
│   │   ├── 📁 schemas/      # Pydantic schemas
│   │   ├── 📁 cache/        # Redis client
│   │   └── main.py          # App entry
│   ├── 📁 tests/            # Pytest
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📁 frontend/             # React Frontend
│   ├── 📁 src/
│   │   ├── 📁 api/          # API clients
│   │   ├── 📁 lib/          # Axios config
│   │   ├── 📁 pages/        # Pages
│   │   ├── 📁 store/        # Zustand stores
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile.dev
│
├── docker-compose.yml
├── LUONG-HE-THONG.md       # System flow explanation
└── README.md
```

## 🔐 Features

- ✅ User Authentication (JWT)
- ✅ User Registration & Login
- ✅ Protected Routes
- ✅ Form Validation
- ✅ API Integration
- ✅ State Management
- ✅ Responsive Design
- ✅ Docker Support
- ✅ Database Migration
- ✅ Redis Caching

## 🌐 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Đăng ký user mới
- `POST /api/v1/auth/login` - Đăng nhập

### Users
- `GET /api/v1/users/` - Lấy danh sách users
- `GET /api/v1/users/{id}` - Lấy thông tin user

Xem đầy đủ tại: http://localhost:8000/docs

## 🗄️ Database

### Thông tin kết nối
```
Host: localhost
Port: 5432
Database: app_db
Username: postgres
Password: postgres
```

### Xem database
```bash
# Command line
docker exec -it postgres_db psql -U postgres -d app_db

# Hoặc click đúp
view-db.bat
```

## 📚 Tài liệu

- **`HUONG-DAN.md`** - Hướng dẫn chi tiết
- **`LUONG-HE-THONG.md`** - Giải thích luồng hoạt động
- **`FIX-VSCODE-ERRORS.md`** - Sửa lỗi VS Code
- **`VIEW-DATABASE.md`** - Cách xem database

## 🧪 Testing

### Backend
```bash
cd backend
pytest
```

### Frontend
```bash
cd frontend
npm run lint
```

## 🐳 Docker Services

- **postgres_db** - PostgreSQL 15
- **redis_cache** - Redis 7
- **fastapi_backend** - Backend API
- **react_frontend** - Frontend UI

## 🔧 Development

### Backend hot-reload
Backend tự động reload khi code thay đổi (uvicorn --reload)

### Frontend hot-reload
Frontend có Vite HMR (Hot Module Replacement)

## 📝 Environment Variables

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

## 🤝 Contributing

Pull requests are welcome!

## 📄 License

MIT License

## 👨‍💻 Author

Your Name

---

⭐ Nếu project hữu ích, hãy cho một star nhé!
