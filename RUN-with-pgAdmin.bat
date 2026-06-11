@echo off
echo ====================================
echo Khoi dong du an Full-Stack + pgAdmin
echo ====================================
echo.
echo Services:
echo   - Frontend: http://localhost:5173
echo   - Backend:  http://localhost:8000
echo   - pgAdmin:  http://localhost:5050
echo.
echo pgAdmin Login:
echo   - Email:    admin@admin.com
echo   - Password: admin
echo.
echo Database Connection Info:
echo   - Host:     postgres
echo   - Port:     5432
echo   - Database: app_db
echo   - Username: postgres
echo   - Password: postgres
echo.
echo ====================================
echo.

docker-compose -f docker-compose-with-pgadmin.yml up --build
