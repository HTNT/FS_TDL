# 🗄️ Các cách xem Database PostgreSQL

## Cách 1: pgAdmin (Giao diện đồ họa) ⭐

### Bước 1: Cài đặt pgAdmin
1. Tải về: https://www.pgadmin.org/download/
2. Cài đặt pgAdmin 4

### Bước 2: Kết nối đến Database
1. Mở pgAdmin
2. Click chuột phải vào "Servers" → "Register" → "Server"
3. Nhập thông tin:
   - **Name:** TDL Project
   - Tab "Connection":
     - **Host:** localhost
     - **Port:** 5432
     - **Database:** app_db
     - **Username:** postgres
     - **Password:** postgres
4. Click "Save"

### Bước 3: Xem dữ liệu
- Mở: Servers → TDL Project → Databases → app_db → Schemas → public → Tables
- Click chuột phải vào bảng "users" → "View/Edit Data" → "All Rows"

---

## Cách 2: DBeaver (Miễn phí, đa nền tảng) ⭐

### Bước 1: Cài đặt DBeaver
1. Tải về: https://dbeaver.io/download/
2. Chọn "DBeaver Community Edition" (miễn phí)

### Bước 2: Kết nối
1. Mở DBeaver
2. Click "New Database Connection" (biểu tượng phích cắm)
3. Chọn "PostgreSQL" → Next
4. Nhập thông tin:
   - **Host:** localhost
   - **Port:** 5432
   - **Database:** app_db
   - **Username:** postgres
   - **Password:** postgres
5. Click "Test Connection" → "Finish"

### Bước 3: Xem dữ liệu
- Mở: PostgreSQL → app_db → Schemas → public → Tables
- Double-click vào bảng "users"

---

## Cách 3: Docker Compose với pgAdmin

Thêm pgAdmin vào docker-compose.yml để chạy cùng dự án:

### File đã tạo: `docker-compose-with-pgadmin.yml`

Chạy bằng lệnh:
```bash
docker-compose -f docker-compose-with-pgadmin.yml up
```

Truy cập: http://localhost:5050
- Email: admin@admin.com
- Password: admin

Sau đó thêm server mới:
- Host: postgres
- Port: 5432
- Database: app_db
- Username: postgres
- Password: postgres

---

## Cách 4: Command Line (psql)

### Từ Docker:
```bash
docker exec -it postgres_db psql -U postgres -d app_db
```

### Lệnh SQL hữu ích:
```sql
-- Xem tất cả bảng
\dt

-- Xem cấu trúc bảng users
\d users

-- Xem dữ liệu trong bảng users
SELECT * FROM users;

-- Đếm số lượng users
SELECT COUNT(*) FROM users;

-- Thoát
\q
```

---

## Cách 5: VS Code Extension

### Bước 1: Cài Extension
1. Mở VS Code
2. Tìm và cài extension: **"PostgreSQL" by Chris Kolkman**

### Bước 2: Kết nối
1. Mở Command Palette (Ctrl+Shift+P)
2. Gõ: "PostgreSQL: Add Connection"
3. Nhập thông tin:
   - Host: localhost
   - Port: 5432
   - Database: app_db
   - Username: postgres
   - Password: postgres

### Bước 3: Xem dữ liệu
- Mở PostgreSQL Explorer trong sidebar
- Expand connection → Tables → Right-click "users" → "Show Table"

---

## Cách 6: Sử dụng script Python

File đã tạo: `scripts/view_database.py`

Chạy:
```bash
cd backend
python scripts/view_database.py
```

---

## Thông tin kết nối:

```
Host: localhost
Port: 5432
Database: app_db
Username: postgres
Password: postgres
```

---

## Khuyến nghị:

✅ **Người mới bắt đầu:** Dùng pgAdmin hoặc DBeaver (giao diện trực quan)
✅ **Developers:** VS Code Extension (tiện lợi nhất)
✅ **Pro users:** Command line (psql)
✅ **Không muốn cài gì thêm:** Docker với pgAdmin
