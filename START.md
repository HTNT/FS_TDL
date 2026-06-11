# Hướng dẫn chạy dự án

## Cách 1: Docker (Khuyến nghị) ⭐

### Yêu cầu:
- Docker Desktop đã cài đặt và đang chạy

### Các bước:

1. **Khởi động tất cả services:**
```bash
docker-compose up --build
```

2. **Đợi tất cả services khởi động xong** (khoảng 2-3 phút lần đầu)

3. **Truy cập ứng dụng:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - PostgreSQL: localhost:5432
   - Redis: localhost:6379

4. **Dừng services:**
```bash
Ctrl + C
```

5. **Xóa containers và volumes:**
```bash
docker-compose down -v
```

---

## Cách 2: Chạy Local

### A. Backend (Terminal 1)

#### Yêu cầu:
- Python 3.11+
- PostgreSQL đang chạy
- Redis đang chạy

#### Các bước:

1. **Di chuyển vào thư mục backend:**
```bash
cd backend
```

2. **Tạo môi trường ảo:**
```bash
python -m venv venv
```

3. **Kích hoạt môi trường ảo:**
```bash
# Windows CMD
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Git Bash hoặc Linux/Mac
source venv/bin/activate
```

4. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

5. **Tạo file .env từ .env.example:**
```bash
copy .env.example .env
```

6. **Chỉnh sửa .env với thông tin database của bạn:**
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-this
```

7. **Chạy backend:**
```bash
uvicorn app.main:app --reload
```

8. **Backend đang chạy tại:** http://localhost:8000

---

### B. Frontend (Terminal 2)

#### Yêu cầu:
- Node.js 18+
- npm

#### Các bước:

1. **Mở terminal mới, di chuyển vào thư mục frontend:**
```bash
cd frontend
```

2. **Cài đặt dependencies:**
```bash
npm install
```

3. **Tạo file .env từ .env.example:**
```bash
copy .env.example .env
```

4. **Chạy frontend:**
```bash
npm run dev
```

5. **Frontend đang chạy tại:** http://localhost:5173

---

## Kiểm tra dự án hoạt động

1. Mở trình duyệt: http://localhost:5173
2. Click "Register" để tạo tài khoản mới
3. Đăng nhập với tài khoản vừa tạo
4. Xem Dashboard với danh sách users

---

## Lệnh hữu ích

### Docker:
```bash
# Xem logs
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f backend
docker-compose logs -f frontend

# Chạy backend tests
docker-compose exec backend pytest

# Restart một service
docker-compose restart backend
```

### Backend Local:
```bash
# Chạy tests
pytest

# Tạo migration mới
alembic revision --autogenerate -m "description"

# Chạy migrations
alembic upgrade head
```

### Frontend Local:
```bash
# Build production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

---

## Khắc phục sự cố

### Docker:
- **Port bị chiếm:** Thay đổi ports trong `docker-compose.yml`
- **Containers không start:** `docker-compose down -v` rồi `docker-compose up --build`
- **Database lỗi:** Xóa volume `docker volume rm tdl_postgres_data`

### Local:
- **Port 8000 bị chiếm:** Thay đổi port trong lệnh uvicorn: `uvicorn app.main:app --port 8001 --reload`
- **Port 5173 bị chiếm:** Thay đổi port trong `vite.config.ts`
- **Database connection error:** Kiểm tra PostgreSQL đang chạy và thông tin trong `.env`
- **Redis connection error:** Kiểm tra Redis đang chạy

---

## Cấu trúc API

### Authentication:
- POST `/api/v1/auth/register` - Đăng ký
- POST `/api/v1/auth/login` - Đăng nhập

### Users:
- GET `/api/v1/users/` - Lấy danh sách users
- GET `/api/v1/users/{id}` - Lấy thông tin user

Xem đầy đủ tại: http://localhost:8000/docs
