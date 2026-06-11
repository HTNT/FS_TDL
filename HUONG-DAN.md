# 🚀 Hướng dẫn chạy dự án

## ⚡ CÁCH NHANH NHẤT - Dùng Docker

### Bước 1: Cài Docker Desktop
1. Tải về: https://www.docker.com/products/docker-desktop/
2. Cài đặt và khởi động Docker Desktop
3. Đợi Docker Desktop khởi động hoàn tất

### Bước 2: Chạy dự án
1. Mở Command Prompt hoặc PowerShell tại thư mục dự án
2. Chạy lệnh:
```bash
docker-compose up --build
```

HOẶC click đúp vào file **RUN.bat**

### Bước 3: Truy cập
- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

Đợi khoảng 2-3 phút cho lần đầu tiên!

---

## 💻 CÁCH 2 - Chạy Local (Không dùng Docker)

### ⚠️ Yêu cầu:
Bạn phải cài đặt và chạy sẵn:
1. **PostgreSQL** (https://www.postgresql.org/download/)
   - Tạo database tên: `app_db`
   - Username: `postgres`
   - Password: `postgres`
   
2. **Redis** (https://github.com/microsoftarchive/redis/releases)
   - Chạy ở port mặc định: 6379

### Bước 1: Setup Backend
1. Mở **Terminal thứ 1** (Command Prompt)
2. Click đúp file **run-backend.bat**
3. Nếu file `.env` chưa có, nó sẽ tự tạo
4. **Chỉnh sửa file `backend/.env`** với thông tin database của bạn
5. Chạy lại **run-backend.bat**

Backend sẽ chạy tại: http://localhost:8000

### Bước 2: Setup Frontend
1. Mở **Terminal thứ 2** (Command Prompt mới)
2. Click đúp file **run-frontend.bat**

Frontend sẽ chạy tại: http://localhost:5173

---

## 📝 Test ứng dụng

1. Mở trình duyệt: http://localhost:5173
2. Click **"Register"** ở menu trên
3. Điền thông tin:
   - Email: test@example.com
   - Username: testuser
   - Password: 123456
4. Click **Register**
5. Quay lại **Login** và đăng nhập
6. Vào **Dashboard** xem danh sách users

---

## ❓ Khắc phục lỗi

### Lỗi Backend:

**❌ "Connection refused" hoặc "could not connect to server"**
- PostgreSQL chưa chạy hoặc thông tin kết nối sai
- Kiểm tra file `backend/.env`
- Đảm bảo PostgreSQL đang chạy

**❌ "redis.exceptions.ConnectionError"**
- Redis chưa chạy
- Chạy Redis server trước

**❌ "Port 8000 is already in use"**
- Port 8000 đang bị chiếm
- Dừng ứng dụng đang dùng port 8000
- Hoặc đổi port: `uvicorn app.main:app --port 8001 --reload`

### Lỗi Frontend:

**❌ "EADDRINUSE: address already in use :::5173"**
- Port 5173 đang bị chiếm
- Dừng ứng dụng đang dùng port 5173

**❌ "Network Error" khi gọi API**
- Backend chưa chạy
- Kiểm tra file `frontend/.env` có `VITE_API_URL=http://localhost:8000`

---

## 📚 Tài liệu thêm

- Chi tiết đầy đủ: **START.md**
- API Documentation: http://localhost:8000/docs (khi backend chạy)

---

## 🎯 Khuyến nghị

**Nếu bạn chưa có kinh nghiệm với PostgreSQL/Redis:**
👉 Dùng Docker Desktop (Cách 1) - Đơn giản và nhanh nhất!

**Nếu bạn đã quen thuộc với development tools:**
👉 Chạy Local (Cách 2) - Linh hoạt hơn cho development
