@echo off
echo ===================================================
echo   ExamForge - Examination Operations System
echo ===================================================
echo.
echo [1/2] Starting Django Backend Server on http://127.0.0.1:8000 ...
start "ExamForge Backend (Django)" cmd /k "python backend\manage.py runserver 127.0.0.1:8000"

echo [2/2] Starting React Vite Frontend on http://localhost:5173 ...
start "ExamForge Frontend (React/Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are launching!
echo UI URL: http://localhost:5173
echo API URL: http://127.0.0.1:8000/api/
echo.
echo Login Credentials:
echo   - Admin: admin / admin123
echo   - Exam Staff: staff1 / staff123
echo   - Faculty: faculty_cs1 / faculty123
echo   - Student: student1 / student123
echo ===================================================
pause
