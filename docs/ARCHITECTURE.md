# ExamForge — System Architecture & 5-Member Module Blueprint

## 1. System Overview

**ExamForge** is a unified, professional-grade examination operations platform designed for universities, colleges, and educational institutions. Built with zero external API dependencies and an educational Forest Green & Ivory aesthetic (strictly free of blue colors).

```
+-------------------------------------------------------------------------------+
|                      ExamForge Frontend (React 18 + Vite)                     |
|  - SaaS Landing Page & Workflow Animations                                    |
|  - Member 3 Timetable Studio (AI Solver, Conflict Radar, Schedule Matrix)     |
|  - Member 2 Academics & Student CSV Importer with Duplicate Detection         |
|  - Member 1 Faculty Directory & Workload Balancer                             |
|  - Member 4 Examination Halls & Seating Matrix Visualizer                     |
|  - Member 5 Local PDF Hall Tickets, Attendance Sheets, and Analytics          |
+-------------------------------------------------------------------------------+
                                        ↕ (Internal REST Endpoints)
+-------------------------------------------------------------------------------+
|                      ExamForge Backend (Django 6 + DRF)                       |
|  ├── apps/accounts (JWT/Session Auth, User Roles, Permissions, UserActivity)  |
|  ├── apps/faculty (FacultyProfile, Workload, Availability Schedules, Leave)   |
|  ├── apps/academics (Department, Course, Branch, Semester, Subject)           |
|  ├── apps/students (Student, Enrollment, SubjectRegistration, CSV Importer)   |
|  ├── apps/examinations (ExamSession, TimeSlot, SubjectConfig, Constraints)    |
|  ├── apps/scheduling (CSP Solver Engine, ConflictAnalyzer, PDF Exporter)      |
|  ├── apps/infrastructure (Block, Room, Usable Exam Capacity, Availability)    |
|  ├── apps/seating (SeatingPlan, RoomAllocation, SeatAssignment Matrix)        |
|  ├── apps/invigilation (InvigilatorDuty, Workload Balance Roster)             |
|  ├── apps/halltickets (HallTicket, Local ReportLab PDF Generator)             |
|  ├── apps/attendance (AttendanceRecord, Room Attendance Sheets, Malpractice)  |
|  ├── apps/notifications (Announcement, SystemNotification Alert Center)       |
|  ├── apps/analytics (Readiness Gauge, Daily Load, Department Heatmaps)        |
|  └── apps/audit (AuditLog, SystemSettings, Immutable Audit Trail)             |
+-------------------------------------------------------------------------------+
                                        ↕ (Django ORM)
+-------------------------------------------------------------------------------+
|                   PostgreSQL Database (Local SQLite Fallback)                 |
+-------------------------------------------------------------------------------+
```

---

## 2. Five-Member Team Responsibility Allocation

### Member 1: Authentication, User & Faculty Management
- **Apps**: `apps.accounts`, `apps.faculty`
- **Deliverables**: Secure authentication, role-based authorization (Admin, Faculty, Staff, Student), faculty availability schedules, leave management.

### Member 2: Student Management, Academic Catalog & Subject Registration
- **Apps**: `apps.academics`, `apps.students`
- **Deliverables**: Departments, courses, branches, semesters, subject credits, student directory, CSV bulk import with duplicate detection, examination eligibility verification.

### Member 3: Examination Configuration & Timetable Generation (Primary Engine)
- **Apps**: `apps.examinations`, `apps.scheduling`
- **Deliverables**: Exam sessions lifecycle, time slots & shift configurator, CSP heuristic constraint solver (MRV + Degree heuristics), live conflict analyzer, manual overrides, revision history, and ReportLab PDF timetable exporter.

### Member 4: Room Infrastructure, Seating Arrangements & Invigilator Allocation
- **Apps**: `apps.infrastructure`, `apps.seating`, `apps.invigilation`
- **Deliverables**: Campus blocks, rooms, usable exam capacity, visual grid seating generator with alternate desk spacing, faculty duty roster with fair workload balancing.

### Member 5: Hall Tickets, Attendance, Reports, Analytics & System Integration
- **Apps**: `apps.halltickets`, `apps.attendance`, `apps.notifications`, `apps.analytics`, `apps.audit`
- **Deliverables**: Local PDF admit pass compiler, room attendance sheets, campus announcements, institutional readiness score, tamper-resistant audit logs, system settings, and complete cross-module integration.
