Write-Host "===================================================" -ForegroundColor Green
Write-Host "   ExamForge - Examination Operations System" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""
Write-Host "[1/2] Starting Django Backend Server on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python backend\manage.py runserver 127.0.0.1:8000"

Write-Host "[2/2] Starting React Vite Frontend on http://localhost:5173 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "Both servers are launching in background windows!" -ForegroundColor Cyan
Write-Host "UI URL: http://localhost:5173" -ForegroundColor White
Write-Host "API URL: http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host ""
Write-Host "Login Credentials:" -ForegroundColor Green
Write-Host "  - Admin:      admin / admin123"
Write-Host "  - Exam Staff: staff1 / staff123"
Write-Host "  - Faculty:    faculty_cs1 / faculty123"
Write-Host "  - Student:    student1 / student123"
Write-Host "===================================================" -ForegroundColor Green
