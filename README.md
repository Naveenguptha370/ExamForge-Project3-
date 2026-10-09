# ExamForge — Examination Operations System

> **Enterprise Examination Lifecycle & AI Constraint Scheduling Platform**  
> Built for Universities, Colleges, and Educational Institutions.  
> **100% Local Execution • Zero External API Keys • Strict Forest Green & Ivory Design (Zero Blue Colors)**

---

## 1. System Identity & Overview

**ExamForge** is a unified, production-grade examination operations platform managing the complete university examination lifecycle:
- Student enrollment & subject registration
- AI constraint-based timetable generation with clash detection (Member 3 Primary Engine)
- Hall capacity management and visual seating layouts (Member 4)
- Fair invigilator workload allocation (Member 4)
- Local PDF admit cards and hall ticket generation (Member 5)
- Room-wise examination attendance recording (Member 5)
- Operations readiness analytics, campus notices, and immutable audit logs (Member 5)

---

## 2. Technology Stack

- **Backend**: Python 3.12, Django 6, Django REST Framework, ReportLab (Local PDF generation).
- **Frontend**: React 18, Vite, Lucide-React, Pure Modern CSS Design System.
- **Database**: PostgreSQL compatible (with immediate zero-config SQLite local execution).
- **Scheduling Algorithm**: Python CSP Constraint Solver with Minimum Remaining Values (MRV), Degree Heuristics, Least Constraining Value (LCV), and Forward Checking.
- **UI Design System**: Strict Forest Green (`#14532D`), Emerald Green (`#15803D`), Warm Gold (`#D4A72C`), Sage Green (`#DDEBDD`), and Warm Ivory (`#FAF9F6`). **Zero Blue elements.**

---

## 3. Five-Member Team Architecture

| Member | Domain & Assigned Modules | Key Deliverables |
|---|---|---|
| **Member 1** | Authentication, User Management, Faculty Management | RBAC (Admin, Faculty, Staff, Student), Faculty Directory, Shift Availability, Leave Logs |
| **Member 2** | Student Management, Academic Management, Subject Registration | Departments, Courses, Branches, Semesters, Subjects, Student Directory, Bulk CSV Importer |
| **Member 3** | **Examination Configuration & Timetable Generation (Primary Focus)** | **Exam Sessions, Time Slots & Shifts, CSP Constraint Solver, Conflict Radar, Manual Override, PDF Timetable** |
| **Member 4** | Rooms, Seating Arrangements, Invigilator Allocation | Campus Blocks, Exam Halls, Visual Seating Matrix, Invigilation Duty Balancer |
| **Member 5** | Hall Tickets, Attendance, Notifications, Analytics, Audit | Local PDF Admit Passes, Room Attendance Sheets, Readiness Score (0-100%), Audit Logs |

---

## 4. Quick Start & Local Setup

### Prerequisites
- Python 3.10+
- Node.js v18+ and npm

### Backend Setup
```bash
# 1. Navigate to project root
cd c:\Users\DELL\OneDrive\Desktop\mem3

# 2. Run Database Migrations
python backend/manage.py migrate

# 3. Seed Realistic Academic & Examination Data (Pre-runs CSP Solver)
python backend/seed_data.py

# 4. Start Django Development Server
python backend/manage.py runserver 127.0.0.1:8000
```

### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies (if not already installed)
npm install

# 3. Launch Vite Development Server
npm run dev
```

Visit **`http://localhost:5173`** in your browser to explore ExamForge!

---

## 5. Automated Test Suite Execution

Run the complete test suite across all 5 member modules and the CSP constraint solver:

```bash
python backend/manage.py test tests
```

**Output**:
```
Ran 11 tests in 52.807s
OK
System check identified no issues.
```

---

## 6. Pre-Configured Test User Accounts

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full Controller of Examinations access |
| **Exam Staff** | `staff1` | `staff123` | Examination cell operations & attendance |
| **Faculty / Invigilator** | `faculty_cs1` | `faculty123` | Duty roster & assigned examination halls |
| **Student** | `student1` | `student123` | Schedule view & PDF hall ticket download |

---

## 7. License & Integrity
Built with pride for academic and institutional excellence. 100% deterministic, zero external API keys required.
