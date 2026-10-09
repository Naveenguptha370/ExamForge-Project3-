"""
ExamForge Institutional Database Seeder.
Populates realistic academic departments, branches, subjects, students, faculty,
rooms, time slots, exam session, and executes the CSP constraint solver.
"""

import os
import sys
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examforge.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import UserRole, UserActivity
from apps.academics.models import Department, Course, Branch, Semester, Subject, DegreeType, SubjectType, DifficultyLevel
from apps.students.models import Student, StudentStatus, StudentEnrollment, SubjectRegistration, EligibilityStatus
from apps.faculty.models import FacultyProfile, Designation, FacultyStatus, FacultyAvailability
from apps.infrastructure.models import Block, Room, RoomType
from apps.examinations.models import ExamSession, SessionType, SessionStatus, TimeSlot, ExamSubjectConfig, SchedulingConstraintConfig
from apps.scheduling.engine.solver import ConstraintTimetableSolver
from apps.audit.models import SystemSetting

User = get_user_model()

def seed_all():
    print("=== Starting ExamForge Institutional Database Seeding ===")

    # 1. System Settings
    SystemSetting.objects.update_or_create(
        key='INSTITUTION_NAME',
        defaults={'value': 'National Institute of Engineering & Technology', 'description': 'Primary Institution Title', 'is_public': True}
    )
    SystemSetting.objects.update_or_create(
        key='ACADEMIC_YEAR',
        defaults={'value': '2025-2026', 'description': 'Current Academic Year', 'is_public': True}
    )
    SystemSetting.objects.update_or_create(
        key='EXAM_CONTROLLER_NAME',
        defaults={'value': 'Dr. K. S. Ramanathan, Ph.D.', 'description': 'Controller of Examinations', 'is_public': True}
    )

    # 2. Users & Roles
    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@examforge.edu',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': UserRole.ADMIN,
            'is_staff': True,
            'is_superuser': True
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()
    print("[OK] Admin user created: admin / admin123")

    staff_user, _ = User.objects.get_or_create(
        username='staff1',
        defaults={
            'email': 'examcell@examforge.edu',
            'first_name': 'Rajesh',
            'last_name': 'Sharma',
            'role': UserRole.EXAM_STAFF,
            'is_staff': True
        }
    )
    staff_user.set_password('staff123')
    staff_user.save()
    print("[OK] Staff user created: staff1 / staff123")

    # 3. Academic Departments
    dept_defs = [
        ('CSE', 'Department of Computer Science & Engineering', 'Prof. Aruna Sundaram', 'cse@examforge.edu'),
        ('ECE', 'Department of Electronics & Communication Engineering', 'Dr. Vikram Seth', 'ece@examforge.edu'),
        ('MECH', 'Department of Mechanical Engineering', 'Dr. Mohan Kumar', 'mech@examforge.edu'),
        ('EEE', 'Department of Electrical & Electronics Engineering', 'Dr. Priya Nambiar', 'eee@examforge.edu'),
        ('CIVIL', 'Department of Civil & Infrastructure Engineering', 'Dr. Anand Verma', 'civil@examforge.edu'),
        ('MATH', 'Department of Mathematics & Computational Sciences', 'Dr. Sunita Rao', 'math@examforge.edu'),
    ]
    dept_objs = {}
    for code, name, hod, email in dept_defs:
        dept, _ = Department.objects.get_or_create(
            code=code,
            defaults={'name': name, 'head_of_department': hod, 'email': email}
        )
        dept_objs[code] = dept
    print(f"[OK] Created {len(dept_objs)} Academic Departments")

    # 4. Courses & Branches
    courses_defs = [
        ('BTECH-CSE', 'B.Tech Computer Science & Engineering', 'CSE', DegreeType.BTECH, 4, 8),
        ('BTECH-ECE', 'B.Tech Electronics & Communication', 'ECE', DegreeType.BTECH, 4, 8),
        ('BTECH-MECH', 'B.Tech Mechanical Engineering', 'MECH', DegreeType.BTECH, 4, 8),
        ('BTECH-EEE', 'B.Tech Electrical Engineering', 'EEE', DegreeType.BTECH, 4, 8),
        ('BTECH-CIVIL', 'B.Tech Civil Engineering', 'CIVIL', DegreeType.BTECH, 4, 8),
        ('MCA', 'Master of Computer Applications', 'CSE', DegreeType.MCA, 2, 4),
    ]
    course_objs = {}
    branch_objs = {}
    for code, name, dept_code, deg, dur, sems in courses_defs:
        course, _ = Course.objects.get_or_create(
            code=code,
            defaults={'name': name, 'department': dept_objs[dept_code], 'degree_type': deg, 'duration_years': dur, 'total_semesters': sems}
        )
        course_objs[code] = course
        
        # Create corresponding primary branch
        b_code = code.replace('BTECH-', '')
        branch, _ = Branch.objects.get_or_create(
            course=course,
            code=b_code,
            defaults={'name': name, 'intake_capacity': 60}
        )
        branch_objs[b_code] = branch
        
        # Create semesters 1 through sems
        for s_num in range(1, sems + 1):
            Semester.objects.get_or_create(
                branch=branch,
                semester_number=s_num,
                academic_year='2025-2026',
                defaults={'term': 'ODD' if s_num % 2 != 0 else 'EVEN', 'is_current': s_num in [1, 3, 5, 7]}
            )
    print(f"[OK] Created {len(course_objs)} Courses & Branches with Semesters")

    # 5. Academic Subjects
    subject_catalog = [
        # CSE Sem 5
        ('CSE', 'CSE', 5, 'CS501', 'Operating Systems & System Architecture', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('CSE', 'CSE', 5, 'CS502', 'Database Management Systems', SubjectType.THEORY, 4.0, DifficultyLevel.MEDIUM),
        ('CSE', 'CSE', 5, 'CS503', 'Theory of Computation & Automata', SubjectType.THEORY, 3.0, DifficultyLevel.HARD),
        ('CSE', 'CSE', 5, 'CS504', 'Computer Networks & Protocols', SubjectType.THEORY, 3.0, DifficultyLevel.MEDIUM),
        ('CSE', 'CSE', 5, 'CS505', 'Design & Analysis of Algorithms', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('CSE', 'CSE', 5, 'CS506', 'Software Engineering & Agile Methodologies', SubjectType.THEORY, 3.0, DifficultyLevel.EASY),
        
        # ECE Sem 5
        ('ECE', 'ECE', 5, 'EC501', 'Digital Signal Processing', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('ECE', 'ECE', 5, 'EC502', 'Microprocessors & Microcontrollers', SubjectType.THEORY, 4.0, DifficultyLevel.MEDIUM),
        ('ECE', 'ECE', 5, 'EC503', 'Electromagnetic Field Waves & Transmission Lines', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('ECE', 'ECE', 5, 'EC504', 'VLSI Design & HDL Modeling', SubjectType.THEORY, 3.0, DifficultyLevel.MEDIUM),
        ('ECE', 'ECE', 5, 'EC505', 'Analog & Digital Communication Systems', SubjectType.THEORY, 4.0, DifficultyLevel.MEDIUM),

        # MECH Sem 5
        ('MECH', 'MECH', 5, 'ME501', 'Design of Machine Elements', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('MECH', 'MECH', 5, 'ME502', 'Applied Thermodynamics & Heat Transfer', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('MECH', 'MECH', 5, 'ME503', 'Manufacturing Technology & CNC Machining', SubjectType.THEORY, 3.0, DifficultyLevel.MEDIUM),
        ('MECH', 'MECH', 5, 'ME504', 'Kinematics & Dynamics of Machinery', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('MECH', 'MECH', 5, 'ME505', 'Fluid Mechanics & Hydraulic Machines', SubjectType.THEORY, 3.0, DifficultyLevel.MEDIUM),

        # EEE Sem 5
        ('EEE', 'EEE', 5, 'EE501', 'Power Systems Analysis & Stability', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('EEE', 'EEE', 5, 'EE502', 'Control Systems Engineering', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('EEE', 'EEE', 5, 'EE503', 'Power Electronics & Inverter Circuits', SubjectType.THEORY, 4.0, DifficultyLevel.MEDIUM),
        ('EEE', 'EEE', 5, 'EE504', 'Electrical Machine Design', SubjectType.THEORY, 3.0, DifficultyLevel.MEDIUM),

        # CIVIL Sem 5
        ('CIVIL', 'CIVIL', 5, 'CE501', 'Structural Analysis & Finite Element Methods', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('CIVIL', 'CIVIL', 5, 'CE502', 'Reinforced Concrete Structures Design', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('CIVIL', 'CIVIL', 5, 'CE503', 'Geotechnical Engineering & Soil Mechanics', SubjectType.THEORY, 4.0, DifficultyLevel.MEDIUM),
        ('CIVIL', 'CIVIL', 5, 'CE504', 'Environmental Engineering & Water Supply', SubjectType.THEORY, 3.0, DifficultyLevel.EASY),

        # Common 1st Year (Sem 1)
        ('MATH', 'CSE', 1, 'MA101', 'Calculus & Linear Algebra', SubjectType.THEORY, 4.0, DifficultyLevel.HARD),
        ('MATH', 'CSE', 1, 'PH101', 'Engineering Physics & Quantum Mechanics', SubjectType.THEORY, 3.0, DifficultyLevel.MEDIUM),
        ('CSE', 'CSE', 1, 'CS101', 'Problem Solving with C Programming', SubjectType.THEORY, 4.0, DifficultyLevel.MEDIUM),
        ('EEE', 'CSE', 1, 'EE101', 'Basic Electrical Engineering', SubjectType.THEORY, 3.0, DifficultyLevel.EASY),
    ]

    subject_objs = {}
    for d_code, b_code, sem_n, s_code, s_name, s_type, credits_v, diff in subject_catalog:
        subj, _ = Subject.objects.get_or_create(
            code=s_code,
            defaults={
                'name': s_name,
                'department': dept_objs[d_code],
                'branch': branch_objs.get(b_code),
                'semester_number': sem_n,
                'subject_type': s_type,
                'credits': credits_v,
                'total_marks': 100,
                'passing_marks': 40,
                'difficulty': diff,
                'is_active': True
            }
        )
        subject_objs[s_code] = subj
    print(f"[OK] Created {len(subject_objs)} Academic Subjects")

    # 6. Faculty Directory & Accounts
    faculty_catalog = [
        ('FAC-CS-01', 'Dr. Anand', 'Krishnan', 'CSE', Designation.PROFESSOR, 'anand.k@examforge.edu'),
        ('FAC-CS-02', 'Mrs. Deepa', 'Menon', 'CSE', Designation.ASSOC_PROF, 'deepa.m@examforge.edu'),
        ('FAC-CS-03', 'Mr. Karthik', 'Raman', 'CSE', Designation.ASST_PROF, 'karthik.r@examforge.edu'),
        ('FAC-CS-04', 'Ms. Sneha', 'Patil', 'CSE', Designation.ASST_PROF, 'sneha.p@examforge.edu'),
        
        ('FAC-EC-01', 'Dr. Suresh', 'Reddy', 'ECE', Designation.PROFESSOR, 'suresh.r@examforge.edu'),
        ('FAC-EC-02', 'Mr. Arvind', 'Swamy', 'ECE', Designation.ASSOC_PROF, 'arvind.s@examforge.edu'),
        ('FAC-EC-03', 'Ms. Divya', 'Nair', 'ECE', Designation.ASST_PROF, 'divya.n@examforge.edu'),

        ('FAC-ME-01', 'Dr. Rangarajan', 'Iyer', 'MECH', Designation.PROFESSOR, 'rangarajan.i@examforge.edu'),
        ('FAC-ME-02', 'Mr. Praveen', 'Kumar', 'MECH', Designation.ASST_PROF, 'praveen.k@examforge.edu'),
        ('FAC-ME-03', 'Mr. Balaji', 'S', 'MECH', Designation.ASST_PROF, 'balaji.s@examforge.edu'),

        ('FAC-EE-01', 'Dr. Meenakshi', 'Sundaram', 'EEE', Designation.PROFESSOR, 'meenakshi.s@examforge.edu'),
        ('FAC-EE-02', 'Ms. Geetha', 'Balan', 'EEE', Designation.ASST_PROF, 'geetha.b@examforge.edu'),

        ('FAC-CE-01', 'Dr. Venkat', 'Prasad', 'CIVIL', Designation.ASSOC_PROF, 'venkat.p@examforge.edu'),
        ('FAC-CE-02', 'Mr. Harish', 'Chandra', 'CIVIL', Designation.ASST_PROF, 'harish.c@examforge.edu'),

        ('FAC-MA-01', 'Dr. Raman', 'Srinivasan', 'MATH', Designation.PROFESSOR, 'raman.s@examforge.edu'),
        ('FAC-MA-02', 'Dr. Lakshmi', 'Narayanan', 'MATH', Designation.ASSOC_PROF, 'lakshmi.n@examforge.edu'),
    ]

    faculty_objs = []
    for emp_id, f_name, l_name, d_code, desig, email in faculty_catalog:
        u_name = f"faculty_{emp_id.lower().replace('-', '_')}"
        fac_user, _ = User.objects.get_or_create(
            username=u_name,
            defaults={
                'email': email,
                'first_name': f_name,
                'last_name': l_name,
                'role': UserRole.FACULTY,
                'department_name': dept_objs[d_code].name,
                'employee_or_roll_id': emp_id
            }
        )
        fac_user.set_password('faculty123')
        fac_user.save()

        profile, _ = FacultyProfile.objects.get_or_create(
            employee_id=emp_id,
            defaults={
                'user': fac_user,
                'first_name': f_name,
                'last_name': l_name,
                'department': dept_objs[d_code],
                'designation': desig,
                'email': email,
                'max_duties_per_session': 8,
                'is_eligible_for_invigilation': True,
                'status': FacultyStatus.ACTIVE
            }
        )
        faculty_objs.append(profile)
    print(f"[OK] Created {len(faculty_objs)} Faculty Members & User Accounts (Password: faculty123)")

    # 7. Examination Rooms & Blocks
    blocks_def = [
        ('NB', 'North Academic Block (Computing & Electronics)', 'North Zone', 4),
        ('SB', 'South Engineering Complex (Mechanical & Civil)', 'South Zone', 4),
        ('RAB', 'Ramanujan Mathematical Science Block', 'Central Campus', 3),
        ('LH', 'Central Lecture Hall Complex', 'East Zone', 2),
    ]
    block_objs = {}
    for b_code, b_name, b_zone, b_floors in blocks_def:
        block, _ = Block.objects.get_or_create(
            code=b_code,
            defaults={'name': b_name, 'campus_zone': b_zone, 'total_floors': b_floors}
        )
        block_objs[b_code] = block

    rooms_def = [
        # North Block
        ('NB', '101', 1, RoomType.EXAM_HALL, 6, 6, 36, 30),
        ('NB', '102', 1, RoomType.EXAM_HALL, 6, 6, 36, 30),
        ('NB', '201', 2, RoomType.EXAM_HALL, 8, 6, 48, 40),
        ('NB', '202', 2, RoomType.EXAM_HALL, 8, 6, 48, 40),
        ('NB', '301', 3, RoomType.EXAM_HALL, 6, 6, 36, 30),
        ('NB', '302', 3, RoomType.EXAM_HALL, 6, 6, 36, 30),

        # South Block
        ('SB', '101', 1, RoomType.EXAM_HALL, 8, 6, 48, 40),
        ('SB', '102', 1, RoomType.EXAM_HALL, 8, 6, 48, 40),
        ('SB', '201', 2, RoomType.EXAM_HALL, 6, 6, 36, 30),
        ('SB', '202', 2, RoomType.EXAM_HALL, 6, 6, 36, 30),

        # Ramanujan Block
        ('RAB', '101', 1, RoomType.EXAM_HALL, 6, 6, 36, 30),
        ('RAB', '102', 1, RoomType.EXAM_HALL, 6, 6, 36, 30),
        ('RAB', '201', 2, RoomType.EXAM_HALL, 8, 6, 48, 40),

        # Central Lecture Halls
        ('LH', 'AUDI-1', 1, RoomType.AUDITORIUM, 12, 10, 120, 100),
        ('LH', 'AUDI-2', 1, RoomType.AUDITORIUM, 12, 10, 120, 100),
    ]
    room_objs = []
    for blk_code, r_num, floor_n, r_type, rows_c, cols_c, tot_cap, usable_cap in rooms_def:
        room, _ = Room.objects.get_or_create(
            block=block_objs[blk_code],
            room_number=r_num,
            defaults={
                'floor_number': floor_n,
                'room_type': r_type,
                'rows_count': rows_c,
                'columns_count': cols_c,
                'total_capacity': tot_cap,
                'usable_exam_capacity': usable_cap,
                'has_cctv': True,
                'is_accessible': True,
                'is_active': True
            }
        )
        room_objs.append(room)
    print(f"[OK] Created {len(room_objs)} Examination Rooms with total usable capacity: {sum(r.usable_exam_capacity for r in room_objs)} seats")

    # 8. Time Slots
    slots_def = [
        ('M1', 'Morning Shift (09:30 AM - 12:30 PM)', 'MORNING', datetime.time(9, 30), datetime.time(12, 30), 180, 1),
        ('A1', 'Afternoon Shift (01:30 PM - 04:30 PM)', 'AFTERNOON', datetime.time(13, 30), datetime.time(16, 30), 180, 2),
        ('E1', 'Evening Shift (05:00 PM - 08:00 PM)', 'EVENING', datetime.time(17, 0), datetime.time(20, 0), 180, 3),
    ]
    slot_objs = {}
    for code, name, shift_v, st, et, dur, s_ord in slots_def:
        slot, _ = TimeSlot.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'shift': shift_v,
                'start_time': st,
                'end_time': et,
                'duration_minutes': dur,
                'sort_order': s_ord,
                'is_active': True
            }
        )
        slot_objs[code] = slot
    print(f"[OK] Created {len(slot_objs)} Shift Time Slots")

    # 9. Students & Subject Registrations (Sem 5 cohort)
    branches_for_cohort = [('CSE', 45), ('ECE', 35), ('MECH', 30), ('EEE', 25), ('CIVIL', 20)]
    student_count = 0
    student_objs = []

    for b_code, count in branches_for_cohort:
        br_obj = branch_objs[b_code]
        for s_idx in range(1, count + 1):
            reg_no = f"23{b_code}{s_idx:03d}"
            email = f"{reg_no.lower()}@student.examforge.edu"
            
            # Create user account for first 5 students in each branch
            student_user = None
            if s_idx <= 2:
                u_name = f"student_{reg_no.lower()}"
                student_user, _ = User.objects.get_or_create(
                    username=u_name,
                    defaults={
                        'email': email,
                        'first_name': f"Student{s_idx}",
                        'last_name': b_code,
                        'role': UserRole.STUDENT,
                        'employee_or_roll_id': reg_no
                    }
                )
                student_user.set_password('student123')
                student_user.save()

            student, _ = Student.objects.get_or_create(
                register_number=reg_no,
                defaults={
                    'user': student_user,
                    'roll_number': f"R-{b_code}-{s_idx:02d}",
                    'first_name': f"Candidate_{s_idx}",
                    'last_name': f"({b_code})",
                    'email': email,
                    'branch': br_obj,
                    'current_semester_number': 5,
                    'admission_year': '2023',
                    'status': StudentStatus.ACTIVE,
                    'is_eligible_for_exams': True
                }
            )
            student_objs.append(student)
            student_count += 1

            # Register student in all Sem 5 subjects of their branch
            branch_subjects = Subject.objects.filter(branch=br_obj, semester_number=5)
            for b_subj in branch_subjects:
                SubjectRegistration.objects.get_or_create(
                    student=student,
                    subject=b_subj,
                    academic_year='2025-2026',
                    defaults={
                        'semester_number': 5,
                        'is_regular': True,
                        'eligibility_status': EligibilityStatus.ELIGIBLE,
                        'attendance_percentage': 82.5 + (s_idx % 15),
                        'is_approved': True
                    }
                )

    print(f"[OK] Created {student_count} Students and registered in Sem 5 curriculum")

    # 10. Member 3: Examination Session & CSP Scheduling Run
    today = datetime.date.today()
    start_d = today + datetime.timedelta(days=14)
    end_d = start_d + datetime.timedelta(days=16)

    exam_session, _ = ExamSession.objects.get_or_create(
        code='ESE-AUT-2025',
        defaults={
            'name': 'End Semester Examinations — Autumn Term 2025',
            'academic_year': '2025-2026',
            'term': 'ODD',
            'session_type': SessionType.END_TERM,
            'start_date': start_d,
            'end_date': end_d,
            'status': SessionStatus.DRAFT,
            'created_by': admin_user,
            'description': 'Comprehensive Semester 5 Final Examination series across Engineering departments.',
            'instructions': '1. Hall Ticket and College ID card mandatory.\n2. No programmable electronic gadgets permitted.\n3. Reporting time: 20 minutes prior to shift commencement.'
        }
    )

    # Configure Constraint Config
    SchedulingConstraintConfig.objects.get_or_create(
        session=exam_session,
        defaults={
            'max_exams_per_student_per_day': 1,
            'min_study_gap_days_hard': 1,
            'min_study_gap_days_general': 0,
            'prevent_cross_branch_clashes': True,
            'allow_saturday_exams': True,
            'allow_sunday_exams': False,
            'max_concurrent_rooms': 15,
            'enforce_room_capacity_limits': True
        }
    )

    # Populate ExamSubjectConfigs for all Sem 5 subjects
    sem5_subjects = Subject.objects.filter(semester_number=5, is_active=True)
    for subj in sem5_subjects:
        ExamSubjectConfig.objects.get_or_create(
            session=exam_session,
            subject=subj,
            defaults={
                'expected_students_count': 45 if subj.branch and subj.branch.code == 'CSE' else 35,
                'max_marks': subj.total_marks,
                'passing_marks': subj.passing_marks,
                'question_paper_code': f"QP-AUT25-{subj.code}",
                'difficulty_weight': 4 if subj.difficulty == DifficultyLevel.HARD else 3,
                'is_mandatory': True
            }
        )

    print(f"[OK] Configured Exam Session '{exam_session.code}' with {exam_session.configured_subjects.count()} subjects")

    # 11. Run Constraint Timetable Solver
    print("\n--- Running Member 3 Constraint Timetable Solver Engine ---")
    solver = ConstraintTimetableSolver(exam_session=exam_session, user=admin_user)
    solver_res = solver.solve()
    print(f"[OK] Solver completed in {round(solver_res.duration_ms, 2)}ms with outcome: {solver_res.outcome}")
    print(f"[OK] Result Message: {solver_res.message}")
    print(f"[OK] Timetable Status: {exam_session.timetable.get_status_display()}, Clashes: {exam_session.timetable.clash_count}")

    print("\n=======================================================")
    print(" ExamForge Database Seeding Completed Successfully! ")
    print("=======================================================")

if __name__ == '__main__':
    seed_all()
