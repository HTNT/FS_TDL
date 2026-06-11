@echo off
echo ====================================
echo Ket noi vao PostgreSQL Database
echo ====================================
echo.
echo Dang ket noi vao database 'app_db'...
echo.
echo Lenh huu ich:
echo   \dt          - Xem danh sach bang
echo   \d users     - Xem cau truc bang users
echo   SELECT * FROM users; - Xem du lieu users
echo   \q           - Thoat
echo.
echo ====================================
echo.

docker exec -it postgres_db psql -U postgres -d app_db
