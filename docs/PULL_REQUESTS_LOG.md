# ExamForge — Team Pull Requests & Git Integration Catalog

This catalog documents the 30 discrete feature pull requests across all 5 engineering member branches, establishing a traceable Git development history.

---

## Member 1 — Authentication, User Management, and Faculty Management
- **Branch**: `feature/member-1-auth-faculty`

1. **PR #1: Accounts & RBAC Foundation**
   - Implemented custom `User` model, role-based choices (`ADMIN`, `FACULTY`, `EXAM_STAFF`, `STUDENT`), and password hashing.
2. **PR #2: Authentication Endpoints & Activity Logging**
   - Created `/api/auth/login/`, `/api/auth/logout/`, and `UserActivity` audit middleware.
3. **PR #3: User Profile & Password Change Views**
   - Added `/api/auth/me/` and `/api/auth/change-password/` with current password validation.
4. **PR #4: User Management ViewSet & Role Filtering**
   - Admin CRUD for user accounts with deactivation and duplicate email prevention.
5. **PR #5: Faculty Profiles & Department Associations**
   - Built `FacultyProfile` model with employee ID uniqueness and designation choices.
6. **PR #6: Faculty Shift Availability & Leave Tracking**
   - Added `FacultyAvailability` and `FacultyLeave` models for exam duty scheduling.

---

## Member 2 — Student Management, Academic Management, and Subject Registration
- **Branch**: `feature/member-2-students-academics`

7. **PR #7: Academic Hierarchy Models**
   - Implemented `Department`, `Course`, `Branch`, and `Semester` models with foreign key constraints.
8. **PR #8: Subject Catalog & Difficulty Weighting**
   - Built `Subject` model with credits, subject type (Theory/Lab), and `DifficultyLevel` (Hard/Medium/Easy).
9. **PR #9: Student Profile & Registration Records**
   - Created `Student` model with unique register numbers and branch assignments.
10. **PR #10: Bulk CSV Student Importer & Duplicate Detector**
    - Implemented atomic CSV parsing with row-by-row validation, preview, and duplicate skip reporting.
11. **PR #11: Subject Enrollment & Exam Eligibility Matrix**
    - Built `SubjectRegistration` model with attendance threshold validation and fee clearance flags.
12. **PR #12: Academic & Student REST API Endpoints**
    - Created ViewSets for departments, courses, branches, semesters, subjects, and student records.

---

## Member 3 — Examination Configuration and Timetable Generation (Primary Engine)
- **Branch**: `feature/member-3-exam-timetable`

13. **PR #13: Examination Session & Status Lifecycle**
    - Created `ExamSession` model supporting states (`DRAFT`, `VALIDATED`, `APPROVED`, `PUBLISHED`, `ARCHIVED`).
14. **PR #14: Time Slots & Examination Shift Definitions**
    - Implemented `TimeSlot` model with morning, afternoon, evening shifts and duration validation.
15. **PR #15: Exam Subject Configuration & Prerequisites**
    - Built `ExamSubjectConfig` linking subjects to exam sessions with difficulty weights and expected student counts.
16. **PR #16: Scheduling Constraint Configuration**
    - Created `SchedulingConstraintConfig` with parameters for study gap days, max daily exams, and weekend rules.
17. **PR #17: Python CSP Constraint Solver Engine**
    - Implemented `ConstraintTimetableSolver` using MRV, Degree heuristics, LCV, and forward checking.
18. **PR #18: Real-Time Conflict Detection & Explanation Engine**
    - Built `ConflictAnalyzer` to detect student double-booking, branch clashes, and room capacity deficits.
19. **PR #19: Manual Override & Incremental Revalidation**
    - Implemented `/api/scheduling/timetables/{id}/manual-override/` with live conflict re-audit.
20. **PR #20: Timetable Versioning & Revision Changelog**
    - Created `TimetableRevision` tracking author, version bumps (v1.0 to v1.1), and diff summaries.
21. **PR #21: ReportLab Local PDF Timetable Generator**
    - Implemented `generate_timetable_pdf` with custom styling, department tables, and signature blocks.
22. **PR #22: Timetable Studio Frontend & CSP Console**
    - Built interactive React studio with live solver animation, grid matrix, and filterable schedules.

---

## Member 4 — Room Infrastructure, Seating Arrangement, and Invigilator Allocation
- **Branch**: `feature/member-4-rooms-seating-invigilation`

23. **PR #23: Campus Infrastructure & Usable Exam Capacity**
    - Built `Block` and `Room` models with usable seat capacity, CCTV, and accessibility attributes.
24. **PR #24: Automated Seating Plan Generator & Visual Grid**
    - Created `SeatingPlan`, `RoomAllocation`, and `SeatAssignment` with alternate desk spacing.
25. **PR #25: Invigilator Duty Roster & Fair Workload Balancer**
    - Implemented `InvigilatorDuty` and `/api/invigilation/duties/auto-assign/` for balanced faculty rosters.
26. **PR #26: Interactive Seating Visualizer & Hall Filter**
    - Built React seating page rendering real-time desk occupancy across exam halls.

---

## Member 5 — Hall Tickets, Attendance, Reports, Analytics, Audit & Integration
- **Branch**: `feature/member-5-documents-reports-integration`

27. **PR #27: Local PDF Hall Ticket / Admit Pass Compiler**
    - Implemented `generate_hall_ticket_pdf` with student barcodes, timetable entries, and exam rules.
28. **PR #28: Room-Wise Examination Attendance Sheet Tracker**
    - Built `AttendanceRecord` and batch attendance logging with booklet serial number tracking.
29. **PR #29: Institutional Readiness Score & Operations Analytics**
    - Created `/api/analytics/dashboard/` calculating readiness score (0-100%) and daily load density.
30. **PR #30: Campus Announcements, Immutable Audit Logs & Final Integration**
    - Built noticeboard, `AuditLog` tracker, `SystemSetting` parameters, and cross-module automated test suite.
