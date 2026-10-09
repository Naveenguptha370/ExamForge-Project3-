# ExamForge — Examination Operations System

> **Enterprise Examination Lifecycle & Operations Management Platform for Higher Education Institutions**
> Designed and implemented across a five-member collaborative engineering team.

---

## 1. Project Identity & Overview

**ExamForge** is a production-grade, secure, full-stack examination operations platform engineered for universities, colleges, and autonomous educational boards. It eliminates the manual friction and scheduling hazards inherent in paper-based examination management by automating the entire lifecycle from curriculum setup to timetable constraint solving, visual seating allocations, fair invigilator rosters, tamper-evident hall ticket PDF generation, and real-time attendance audits.

### Core Architectural Principles

- **Frontend:** React.js, HTML5, Vanilla CSS Design System, Lucide Icons, Vite.
- **Backend:** Python 3.12, Django 5.1, Django REST Framework.
- **Database:** PostgreSQL (production ready) / SQLite (zero-dependency local development).
- **Constraint Solver Engine:** Native Python heuristic constraint satisfaction algorithm using MRV (Minimum Remaining Values / Most-Constrained-First) and backtracking.
- **Local PDF Generation:** High-resolution admit cards and examination attendance sheets compiled locally via ReportLab.
- **Zero Third-Party APIs:** Complete self-contained operation on institutional servers with zero external API dependencies (no external SaaS subscriptions, no external cloud keys).
- **Strict Color Restraint (No Blue Policy):** Sophisticated green and warm ivory palette (`#14532D`, `#15803D`, `#DDEBDD`, `#F59E0B`, `#D4A72C`, `#FAF9F6`). Absolutely no blue UI components.
- **Real Database Operations:** No hardcoded dashboard statistics, fake mock saves, or simulated database states.

---

## 2. Five-Member Team Module Allocation

The system architecture cleanly partitions responsibilities across 5 engineering members, integrated into one unified web application:

| Member | Subsystem & Assigned Modules | Deliverables |
| :--- | :--- | :--- |
| **Member 1** | **Authentication, User Management & Faculty Management** | Custom User model extending `AbstractUser` with 4 RBAC roles (`ADMIN`, `FACULTY`, `EXAM_STAFF`, `STUDENT`), Token Authentication, password management, user activity logging, faculty profiles, availability schedules, and leave approval workflows. |
| **Member 2** | **Academic Management, Student Registry & Exam Registration** | Curriculum hierarchy (Departments, Courses, Branches, Semesters, Subjects with credits), Student Profile registry, bulk CSV import engine with row-by-row preview and validation, duplicate detection, subject registrations, and attendance shortage eligibility calculations (<75%). |
| **Member 3** | **Examination Configuration & Timetable Scheduling** | Examination session configuration (Regular, Supplementary, Mid-Term), time slots, Exam Subjects, Python heuristic constraint solver with student conflict graph, double-booking prevention, timetable approval, and multi-channel publication. |
| **Member 4** | **Infrastructure, Seating Arrangements & Invigilator Allocation** | Academic blocks, examination hall registry, usable capacity with exam spacing rules, visual row/column seating grid, alternate column spacing algorithm, capacity shortage warnings, and fair invigilator duty allocation roster. |
| **Member 5** | **Hall Tickets, Attendance, Analytics, Audit Logs, Settings & Final Integration** | Local ReportLab PDF generation engine, individual/bulk hall ticket issuance, eligibility verification gate, examination hall attendance recording, answer booklet tracking, correction audit trails, executive analytics, readiness index, and end-to-end integration. |

---

## 3. UI Design System — Zero Blue Palette

The visual identity follows a sophisticated, human-designed aesthetic tailored for educational governance:

- **Deep Forest Green:** `#14532D` (Primary brand color, headers, master CTAs)
- **Emerald Green:** `#15803D` (Sub-headers, active state indicators, success badges)
- **Sage Green:** `#DDEBDD` (Secondary button backgrounds, table alternating row highlights)
- **Warm Amber:** `#F59E0B` (Warning badges, slot alerts)
- **Premium Gold:** `#D4A72C` (Accents, special badges, brand crest)
- **Warm Ivory Background:** `#FAF9F6` (Page body canvas)
- **White Card Canvas:** `#FFFFFF` (Surface container, tables, modals)
- **Charcoal Text:** `#242923` (High readability body typography)
- **Muted Slate Gray:** `#6B7280` (Labels, captions, timestamps)
- **Neutral Borders:** `#E7E5E4` (Structural dividers and table grid lines)

---

## 4. End-to-End Examination Lifecycle Workflow

1. **Administration & Auth:** Administrator logs into the central console. User accounts, roles, and faculty records are active.
2. **Curriculum & Academic Catalog:** Departments (CSE, ECE, MECH, CIVIL), degree courses, branches, semesters, and subject papers are registered.
3. **Student Enrollment & Bulk CSV:** Students are registered individually or bulk-imported via CSV with duplicate roll number checks.
4. **Subject Registrations:** Students enroll in academic subjects. Attendance percentages are tracked; students with <75% attendance are automatically flagged as `ATTENDANCE_SHORTAGE`.
5. **Session Configuration:** Examination session is configured (e.g. `ESE-MAY-2026`) with date boundaries and official time slots.
6. **Constraint Solver Engine:** The native Python scheduler inspects student enrollments, constructs a conflict graph, and schedules subjects into conflict-free dates and slots with zero student clashes.
7. **Timetable Approval & Publication:** The Controller of Examinations reviews the draft timetable and signs off, publishing the schedule.
8. **Infrastructure & Hall Allocation:** Available examination rooms are selected according to usable exam spacing capacity.
9. **Visual Seating Allocation:** Students are automatically seated with alternate-column spacing (`ALTERNATE_COLS`), ensuring candidates sitting side-by-side do not write the same paper.
10. **Invigilator Duty Assignment:** Available faculty are automatically allocated to rooms based on fair workload balance and leave status.
11. **Hall Ticket Generation (ReportLab PDF):** High-resolution admit cards with unique security verification hashes, seating coordinates, and exam rules are generated locally.
12. **Examination Hall Attendance:** Invigilators record physical attendance (Present, Absent, Late, Malpractice) and answer booklet serial numbers.
13. **Attendance Correction Audit:** Any subsequent correction to submitted attendance requires an authorized reason and is permanently logged into `AttendanceCorrectionAudit`.
14. **Executive Reporting & Analytics:** Comprehensive executive reports, room utilization breakdowns, and lifecycle readiness metrics are compiled and exportable as CSV and ReportLab PDFs.

---

## 5. Local Setup & Quickstart Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Node.js v18+ (Tested on Node.js v24)
- Git

### A. Backend Setup (Django + DRF)

```bash
# 1. Navigate to backend directory
cd backend

# 2. (Optional) Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Apply database migrations
python manage.py migrate

# 4. Seed comprehensive university demo dataset
python seed_demo_data.py

# 5. Run automated test suites
python manage.py test tests

# 6. Start Django backend server (runs on http://localhost:8000)
python manage.py runserver 0.0.0.0:8000
```

To add 100 additional students for the 2026-2027 academic year without changing
the existing examination-session dataset, run this optional, rerunnable seed:

```bash
python seed_demo_data.py --extended-students
```

### B. Frontend Setup (React + Vite)

```bash
# 1. In a separate terminal, navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server (runs on http://localhost:5173)
npm run dev
```

Open your browser at **`http://localhost:5173`** to access the application.

---

## 6. One-Click Evaluator Demo Credentials

ExamForge includes a pre-seeded institutional dataset with instant demo credentials:

| Role | Username | Password | Purpose & Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full institutional authority: user management, faculty assignments, timetable solver approval, seating allocation, system settings, and executive PDF reporting. |
| **Examination Staff** | `examstaff` | `staff123` | Examination operations: student registries, CSV imports, room allocations, hall attendance records, and admit cards. |
| **Faculty / Invigilator** | `prof.sharma` | `faculty123` | Faculty duties: view assigned examination halls, supervise attendance sheets, and submit leave applications. |
| **Student** | `student.24cs101` | `student123` | Student portal: view published examination timetable, assigned examination hall, seat label, and download verified Hall Ticket PDF. |

*Tip:* Use the **"One-Click Evaluator Roles"** switcher in the login screen or sidebar for instant switching without re-typing passwords!

---

## 7. Automated Testing Suite

The repository contains 15 automated test suites covering all member subsystems:

```bash
cd backend
python manage.py test tests
```

### Test Coverage Highlights
- `test_member1_auth_faculty.py`: Token authentication, invalid credentials, deactivated account gatekeeping, faculty profile summaries, and leave approvals.
- `test_member2_academics_students.py`: Unique roll/registration constraints, duplicate subject registration prevention, and automatic attendance shortage calculations.
- `test_member3_scheduling_solver.py`: Constraint heuristic engine, student double-booking clash prevention, and timetable approval validation.
- `test_member4_infrastructure_seating.py`: Room capacity rules, duplicate seat allocation detection, and student assignment uniqueness.
- `test_member5_documents_lifecycle.py`: Local binary ReportLab PDF generation, hall ticket ineligibility blocking, attendance correction audit trails, and examination readiness indices.

---

## 8. Verified GitHub Pull Requests

As of October 9, 2026, the repository has **3 pull requests**, and all three
were merged into `main`:

- [PR #1 — Harden account and faculty access controls](https://github.com/Naveenguptha370/ExamForge-Project3-/pull/1)
- [PR #2 — Attendence management](https://github.com/Naveenguptha370/ExamForge-Project3-/pull/2)
- [PR #3 — Member 4 room infrastructure, seating, and invigilation integration](https://github.com/Naveenguptha370/ExamForge-Project3-/pull/3)

This list reflects verified GitHub pull requests; it does not count feature
branches or commits as pull requests.

---

## 9. Contributors & Core Engineering Team

ExamForge is developed and maintained by:

- **Pernamitta Sumanth Reddy** ([@pernamittasumanthreddy](https://github.com/pernamittasumanthreddy)) — Lead Engineer: Infrastructure, Seating Arrangement Engine, Room Synchronization & Invigilator Rostering (Member 4)
- **Pavan Kalyan Vallabhaneni** ([@pavankalyanvallabhaneni8](https://github.com/pavankalyanvallabhaneni8)) — Attendance Management, Answer Booklet Logging & Examination Operations
- **Naveen Guptha** ([@Naveenguptha370](https://github.com/Naveenguptha370)) — Project Lead, Architecture & Core Coordination

---

## 10. License & Institutional Copyright

© 2026 ExamForge Academic Consortium. Built for higher education administration excellence.
