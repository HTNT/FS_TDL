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

## 🐳 Docker Services

- **postgres_db** - PostgreSQL 15
- **redis_cache** - Redis 7
- **fastapi_backend** - Backend API
- **react_frontend** - Frontend UI

