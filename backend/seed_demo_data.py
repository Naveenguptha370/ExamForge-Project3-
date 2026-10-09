"""
ExamForge - Database Seeder Script
Populates a comprehensive realistic university examination operations dataset.
"""

import argparse
import os
import sys
import django
from datetime import date, time, timedelta
from django.db import transaction

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examforge.settings')
django.setup()

from apps.accounts.models import User, UserActivityLog
from apps.faculty.models import FacultyProfile, FacultyAvailability, FacultyLeave
from apps.academics.models import Department, Course, Branch, Semester, Subject
from apps.students.models import StudentProfile
from apps.registration.models import StudentEnrollment, SubjectRegistration
from apps.examinations.models import ExamSession, TimeSlot, ExamSubject
from apps.scheduling.models import Timetable, TimetableEntry, SchedulingConflict
from apps.scheduling.solver import TimetableSchedulerEngine
from apps.infrastructure.models import Building, ExaminationRoom, RoomAvailability
from apps.seating.models import Seat, SeatingPlan, SeatAllocation
from apps.invigilation.models import InvigilatorDuty
from apps.halltickets.models import HallTicket, HallTicketEntry
from apps.halltickets.pdf_generator import generate_hall_ticket_pdf
from apps.attendance.models import ExamAttendanceSheet, AttendanceRecord, AttendanceCorrectionAudit
from apps.notifications.models import Announcement, InAppNotification
from apps.audit.models import AuditLog
from apps.system_settings.models import SystemSetting
from django.core.files.base import ContentFile


@transaction.atomic
def run_extended_student_seed():
    """Create an isolated, repeatable 100-student dataset for the next academic year."""
    print("[*] Seeding 100 additional students for academic-year testing...")

    department, _ = Department.objects.get_or_create(
        code='CSE',
        defaults={
            'name': 'Computer Science & Engineering',
            'head_of_department': 'Prof. A. K. Sharma',
        },
    )
    course, _ = Course.objects.get_or_create(
        code='BTECH',
        defaults={
            'name': 'Bachelor of Technology',
            'department': department,
            'duration_years': 4,
            'degree_type': 'Undergraduate',
        },
    )
    branches = [
        Branch.objects.get_or_create(
            code=code,
            defaults={'name': name, 'course': course},
        )[0]
        for code, name in (
            ('CSE-CORE', 'Computer Science (Core)'),
            ('CSE-AIML', 'Artificial Intelligence & Machine Learning'),
            ('CSE-DS', 'Data Science & Analytics'),
        )
    ]
    semester, _ = Semester.objects.get_or_create(
        number=2,
        academic_year='2026-2027',
        term=Semester.Term.ODD,
    )

    subjects = [
        Subject.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'department': department,
                'branch': branches[index % len(branches)],
                'semester': semester,
                'credits': credits,
                'min_attendance_pct': 75,
            },
        )[0]
        for index, (code, name, credits) in enumerate((
            ('CSE201', 'Programming Fundamentals', 4.0),
            ('CSE202', 'Discrete Mathematics', 4.0),
            ('CSE203', 'Digital Logic Design', 3.0),
            ('CSE204', 'Engineering Communication', 2.0),
        ))
    ]

    first_names = (
        'Aarav', 'Ananya', 'Rohan', 'Diya', 'Sai',
        'Ishaan', 'Kavya', 'Aditya', 'Neha', 'Vikram',
    )
    last_names = (
        'Sharma', 'Reddy', 'Verma', 'Rao', 'Nair',
        'Patel', 'Gupta', 'Iyer', 'Mishra', 'Pillai',
    )

    for index in range(100):
        roll_number = f'26CS{201 + index:03d}'
        username = f'student.{roll_number.lower()}'
        first_name = first_names[index % len(first_names)]
        last_name = last_names[(index // len(first_names) + index) % len(last_names)]
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{roll_number.lower()}@student.examforge.edu',
                'first_name': first_name,
                'last_name': last_name,
                'role': User.Role.STUDENT,
            },
        )
        if created:
            user.set_password('student123')
            user.save(update_fields=['password'])

        student, _ = StudentProfile.objects.get_or_create(
            registration_no=f'REG2026{1201 + index:04d}',
            defaults={
                'user': user,
                'roll_no': roll_number,
                'first_name': first_name,
                'last_name': last_name,
                'email': f'{roll_number.lower()}@student.examforge.edu',
                'department': department,
                'course': course,
                'branch': branches[index % len(branches)],
                'semester': semester,
                'admission_year': 2026,
                'status': StudentProfile.Status.ACTIVE,
                'contact_phone': f'+91 97100 {10000 + index:05d}',
                'is_eligible_for_exam': index % 20 != 0,
            },
        )
        StudentEnrollment.objects.get_or_create(
            student=student,
            semester=semester,
            academic_year='2026-2027',
        )

        for subject_index, subject in enumerate(subjects):
            attendance = (
                68.0
                if index % 20 == 0 and subject_index == 0
                else 80.0 + ((index * 7 + subject_index * 11) % 21)
            )
            SubjectRegistration.objects.get_or_create(
                student=student,
                subject=subject,
                semester=semester,
                defaults={
                    'is_approved': True,
                    'attendance_percentage': attendance,
                    'internal_marks': 18.0 + ((index + subject_index) % 13),
                },
            )

    print("  [+] Added 100 students, 100 semester enrollments, and 400 subject registrations.")
    print("  [+] Five students have an attendance-shortage example for eligibility testing.")


def run_seed():
    print("[*] Starting ExamForge Comprehensive Database Seeding...")

    # 1. System Settings
    setting, _ = SystemSetting.objects.get_or_create(id=1, defaults={
        'institution_name': 'ExamForge Institute of Technology',
        'institution_code': 'EFIT-HYD',
        'academic_year': '2025-2026',
        'current_term': 'EVEN',
        'contact_email': 'controller.exams@examforge.edu',
        'contact_phone': '+91 40 2345 6789',
        'address': 'Campus Park, Tech Boulevard, Hyderabad, Telangana 500081',
        'min_attendance_threshold': 75,
        'default_exam_duration_mins': 180,
        'default_spacing_rule': 'ALTERNATE_COLS'
    })
    print("  [+] System Settings configured")

    # 2. User Accounts
    # Admin
    admin_user, _ = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@examforge.edu',
        'first_name': 'Dr. K. S.',
        'last_name': 'Rajeshwar',
        'role': User.Role.ADMIN,
        'is_staff': True,
        'is_superuser': True
    })
    admin_user.set_password('admin123')
    admin_user.save()

    # Exam Staff
    staff_user, _ = User.objects.get_or_create(username='examstaff', defaults={
        'email': 'staff@examforge.edu',
        'first_name': 'Suresh',
        'last_name': 'Verma',
        'role': User.Role.EXAM_STAFF,
        'is_staff': True
    })
    staff_user.set_password('staff123')
    staff_user.save()

    print("  [+] Core administrative accounts created (admin/admin123, examstaff/staff123)")

    # 3. Academics: Departments
    dept_cse, _ = Department.objects.get_or_create(code='CSE', defaults={
        'name': 'Computer Science & Engineering',
        'head_of_department': 'Prof. A. K. Sharma',
        'description': 'Department of Computing, AI, Data Science & Software Engineering'
    })
    dept_ece, _ = Department.objects.get_or_create(code='ECE', defaults={
        'name': 'Electronics & Communication Engineering',
        'head_of_department': 'Prof. V. Reddy',
        'description': 'VLSI, Embedded Systems, Signal Processing & Telecommunications'
    })
    dept_mech, _ = Department.objects.get_or_create(code='MECH', defaults={
        'name': 'Mechanical Engineering',
        'head_of_department': 'Prof. M. Patel',
        'description': 'Thermal, Robotics, Manufacturing & Automation'
    })
    dept_civil, _ = Department.objects.get_or_create(code='CIVIL', defaults={
        'name': 'Civil & Structural Engineering',
        'head_of_department': 'Prof. R. Gupta',
        'description': 'Structural Mechanics, Geotechnical & Urban Infrastructure'
    })

    # Courses & Branches
    course_btech, _ = Course.objects.get_or_create(code='BTECH', defaults={
        'name': 'Bachelor of Technology',
        'department': dept_cse,
        'duration_years': 4,
        'degree_type': 'Undergraduate'
    })

    branch_ai, _ = Branch.objects.get_or_create(code='CSE-AIML', defaults={'name': 'Artificial Intelligence & Machine Learning', 'course': course_btech})
    branch_ds, _ = Branch.objects.get_or_create(code='CSE-DS', defaults={'name': 'Data Science & Analytics', 'course': course_btech})
    branch_core, _ = Branch.objects.get_or_create(code='CSE-CORE', defaults={'name': 'Computer Science (Core)', 'course': course_btech})
    branch_ece, _ = Branch.objects.get_or_create(code='ECE-CORE', defaults={'name': 'Electronics Engineering', 'course': course_btech})

    # Semesters
    sem4, _ = Semester.objects.get_or_create(number=4, academic_year='2025-2026', term=Semester.Term.EVEN, defaults={'is_current': True})
    sem6, _ = Semester.objects.get_or_create(number=6, academic_year='2025-2026', term=Semester.Term.EVEN, defaults={'is_current': False})

    # Subjects for Sem 4
    sub1, _ = Subject.objects.get_or_create(code='CS401', defaults={
        'name': 'Design & Analysis of Algorithms',
        'department': dept_cse,
        'branch': branch_core,
        'semester': sem4,
        'credits': 4.0,
        'min_attendance_pct': 75
    })
    sub2, _ = Subject.objects.get_or_create(code='CS402', defaults={
        'name': 'Operating Systems & System Programming',
        'department': dept_cse,
        'branch': branch_core,
        'semester': sem4,
        'credits': 4.0,
        'min_attendance_pct': 75
    })
    sub3, _ = Subject.objects.get_or_create(code='CS403', defaults={
        'name': 'Database Management Systems & SQL',
        'department': dept_cse,
        'branch': branch_ai,
        'semester': sem4,
        'credits': 3.5,
        'min_attendance_pct': 75
    })
    sub4, _ = Subject.objects.get_or_create(code='EC401', defaults={
        'name': 'Microprocessors & Microcontrollers',
        'department': dept_ece,
        'branch': branch_ece,
        'semester': sem4,
        'credits': 4.0,
        'min_attendance_pct': 75
    })
    sub5, _ = Subject.objects.get_or_create(code='MA401', defaults={
        'name': 'Probability, Statistics & Queueing Theory',
        'department': dept_cse,
        'branch': branch_ds,
        'semester': sem4,
        'credits': 3.0,
        'min_attendance_pct': 75
    })
    print("  [+] Academic hierarchy created (Departments, Courses, Branches, Semesters, Subjects)")

    # 4. Faculty Profiles
    faculty_data = [
        ('prof.sharma', 'FAC-CSE-001', 'Anand', 'Sharma', dept_cse, FacultyProfile.Designation.PROFESSOR, 'Ph.D in Machine Learning'),
        ('prof.reddy', 'FAC-CSE-002', 'Venkata', 'Reddy', dept_cse, FacultyProfile.Designation.ASSOC_PROFESSOR, 'Ph.D in Distributed Systems'),
        ('prof.iyer', 'FAC-ECE-001', 'Lakshmi', 'Iyer', dept_ece, FacultyProfile.Designation.PROFESSOR, 'Ph.D in VLSI Design'),
        ('prof.patel', 'FAC-MECH-001', 'Manish', 'Patel', dept_mech, FacultyProfile.Designation.ASSOC_PROFESSOR, 'M.Tech, Thermal Sciences'),
        ('prof.gupta', 'FAC-MATH-001', 'Sunita', 'Gupta', dept_cse, FacultyProfile.Designation.ASST_PROFESSOR, 'Ph.D in Applied Mathematics'),
        ('prof.chatterjee', 'FAC-CSE-003', 'Subhash', 'Chatterjee', dept_cse, FacultyProfile.Designation.ASST_PROFESSOR, 'M.Tech, Cybersecurity'),
    ]

    faculties = []
    for uname, emp_id, fname, lname, dept, desig, qual in faculty_data:
        u, _ = User.objects.get_or_create(username=uname, defaults={
            'email': f'{uname}@examforge.edu',
            'first_name': fname,
            'last_name': lname,
            'role': User.Role.FACULTY
        })
        u.set_password('faculty123')
        u.save()

        f_prof, _ = FacultyProfile.objects.get_or_create(user=u, defaults={
            'employee_id': emp_id,
            'department': dept,
            'designation': desig,
            'qualification': qual,
            'phone': '+91 98480 12345',
            'max_duties_per_term': 8,
            'is_available_for_duty': True
        })
        faculties.append(f_prof)

    print(f"  [+] {len(faculties)} Faculty profiles and invigilator accounts initialized (password: faculty123)")

    # 5. Students & Enrollments
    # Create 25 realistic students
    first_names = ["Aarav", "Ananya", "Rohan", "Diya", "Sai", "Ishaan", "Kavya", "Aditya", "Neha", "Vikram",
                   "Pooja", "Arjun", "Sneha", "Rahul", "Tanvi", "Naveen", "Meera", "Varun", "Rhea", "Kiran",
                   "Deepak", "Anjali", "Gautam", "Shruti", "Pranav"]
    last_names = ["Kalyan", "Sharma", "Reddy", "Verma", "Rao", "Nair", "Patel", "Gupta", "Deshmukh", "Choudhury",
                  "Joshi", "Bose", "Mehta", "Iyer", "Mishra", "Pillai", "Menon", "Saxena", "Chauhan", "Bhat",
                  "Pandey", "Kapoor", "Mukherjee", "Swaminathan", "Yadav"]

    students = []
    for i in range(25):
        roll = f"24CS{101 + i:03d}"
        reg = f"REG2024{1001 + i:04d}"
        fname = first_names[i]
        lname = last_names[i]
        uname = f"student.{roll.lower()}"

        u, _ = User.objects.get_or_create(username=uname, defaults={
            'email': f"{roll.lower()}@student.examforge.edu",
            'first_name': fname,
            'last_name': lname,
            'role': User.Role.STUDENT
        })
        u.set_password('student123')
        u.save()

        # Mark 2 students as attendance shortage / ineligible for testing Member 2 & Member 5 edge cases
        is_eligible = (i not in [23, 24])

        s_prof, _ = StudentProfile.objects.get_or_create(registration_no=reg, defaults={
            'user': u,
            'roll_no': roll,
            'first_name': fname,
            'last_name': lname,
            'email': f"{roll.lower()}@student.examforge.edu",
            'department': dept_cse,
            'course': course_btech,
            'branch': branch_core if i % 2 == 0 else branch_ai,
            'semester': sem4,
            'admission_year': 2024,
            'status': StudentProfile.Status.ACTIVE,
            'contact_phone': f'+91 97000 {10000 + i}',
            'is_eligible_for_exam': is_eligible
        })
        students.append(s_prof)

        # Enroll in semester
        StudentEnrollment.objects.get_or_create(student=s_prof, semester=sem4, academic_year='2025-2026')

        # Register for Sem 4 subjects
        for sub in [sub1, sub2, sub3, sub5]:
            att_pct = 88.0 if is_eligible else 62.0
            elig = SubjectRegistration.EligibilityStatus.ELIGIBLE if is_eligible else SubjectRegistration.EligibilityStatus.ATTENDANCE_SHORTAGE
            SubjectRegistration.objects.get_or_create(
                student=s_prof,
                subject=sub,
                semester=sem4,
                defaults={
                    'is_approved': True,
                    'eligibility_status': elig,
                    'attendance_percentage': att_pct,
                    'internal_marks': 24.5
                }
            )

    print(f"  [+] {len(students)} Student profiles enrolled in 4 core subjects with attendance tracking")

    # 6. Examination Session
    session, _ = ExamSession.objects.get_or_create(session_code='ESE-MAY-2026', defaults={
        'name': 'End Semester Examinations May 2026',
        'academic_year': '2025-2026',
        'term': 'EVEN',
        'session_type': ExamSession.SessionType.REGULAR,
        'start_date': date(2026, 5, 11),
        'end_date': date(2026, 5, 23),
        'status': ExamSession.Status.PUBLISHED,
        'created_by': admin_user,
        'instructions': 'Admit Card mandatory. Arrive 20 mins before commencement. No electronic devices.'
    })

    # Time Slots
    slot_morning, _ = TimeSlot.objects.get_or_create(slot_code='SLOT-FN', defaults={
        'name': 'Forenoon Session (FN)',
        'start_time': time(9, 30),
        'end_time': time(12, 30)
    })
    slot_afternoon, _ = TimeSlot.objects.get_or_create(slot_code='SLOT-AN', defaults={
        'name': 'Afternoon Session (AN)',
        'start_time': time(14, 0),
        'end_time': time(17, 0)
    })

    # Exam Subjects
    es1, _ = ExamSubject.objects.get_or_create(exam_session=session, subject=sub1, defaults={'duration_minutes': 180, 'max_marks': 100})
    es2, _ = ExamSubject.objects.get_or_create(exam_session=session, subject=sub2, defaults={'duration_minutes': 180, 'max_marks': 100})
    es3, _ = ExamSubject.objects.get_or_create(exam_session=session, subject=sub3, defaults={'duration_minutes': 180, 'max_marks': 100})
    es5, _ = ExamSubject.objects.get_or_create(exam_session=session, subject=sub5, defaults={'duration_minutes': 180, 'max_marks': 100})
    print("  [+] Examination Session and Time Slots configured")

    # 7. Timetable Constraint Solver Engine
    print("  [*] Running Python Constraint Solver Engine for Timetable...")
    engine = TimetableSchedulerEngine(session.id)
    solve_res = engine.solve()
    print(f"  [+] Solver Result: {solve_res['status']} - {solve_res['message']}")

    # Mark Timetable Approved & Published
    timetable = Timetable.objects.get(exam_session=session)
    timetable.status = Timetable.Status.PUBLISHED
    timetable.approved_by = admin_user
    timetable.approved_at = django.utils.timezone.now()
    timetable.published_at = django.utils.timezone.now()
    timetable.save()

    # 8. Infrastructure: Buildings & Examination Rooms
    bldg_aryabhata, _ = Building.objects.get_or_create(code='ARYA-BLK', defaults={
        'name': 'Aryabhata Academic Complex',
        'floors_count': 4,
        'description': 'Main science and engineering lecture halls'
    })
    bldg_ramanujan, _ = Building.objects.get_or_create(code='RAMAN-TWR', defaults={
        'name': 'Ramanujan Computing Tower',
        'floors_count': 5,
        'description': 'Auditoriums and computing seminar halls'
    })

    room_lh101, _ = ExaminationRoom.objects.get_or_create(room_number='LH-101', defaults={
        'building': bldg_aryabhata,
        'floor': 1,
        'room_type': ExaminationRoom.RoomType.LECTURE_HALL,
        'total_capacity': 60,
        'usable_capacity': 30,
        'rows': 5,
        'columns': 6,
        'has_cctv': True,
        'is_accessible': True,
        'status': ExaminationRoom.Status.AVAILABLE
    })

    room_lh102, _ = ExaminationRoom.objects.get_or_create(room_number='LH-102', defaults={
        'building': bldg_aryabhata,
        'floor': 1,
        'room_type': ExaminationRoom.RoomType.LECTURE_HALL,
        'total_capacity': 60,
        'usable_capacity': 30,
        'rows': 5,
        'columns': 6,
        'has_cctv': True,
        'is_accessible': True,
        'status': ExaminationRoom.Status.AVAILABLE
    })

    room_aud01, _ = ExaminationRoom.objects.get_or_create(room_number='AUD-01', defaults={
        'building': bldg_ramanujan,
        'floor': 1,
        'room_type': ExaminationRoom.RoomType.AUDITORIUM,
        'total_capacity': 120,
        'usable_capacity': 60,
        'rows': 6,
        'columns': 10,
        'has_cctv': True,
        'is_accessible': True,
        'status': ExaminationRoom.Status.AVAILABLE
    })
    print("  [+] Examination Infrastructure & Halls registered (LH-101, LH-102, AUD-01)")

    # 9. Seating Arrangement Generation
    print("  [*] Generating Seating Plans with Alternate Column Spacing...")
    eligible_students = [s for s in students if s.is_eligible_for_exam]

    for es in [es1, es2, es3, es5]:
        # Generate seats for LH-101 if not exist
        Seat.objects.filter(room=room_lh101).delete()
        seats = []
        for r in range(1, room_lh101.rows + 1):
            for c in range(1, room_lh101.columns + 1):
                seats.append(Seat(room=room_lh101, row_num=r, col_num=c, seat_label=f"{chr(64+r)}{c}", is_usable=True))
        Seat.objects.bulk_create(seats)

        usable_seats = Seat.objects.filter(room=room_lh101, col_num__in=[1, 3, 5]).order_by('row_num', 'col_num')

        plan, _ = SeatingPlan.objects.get_or_create(
            exam_subject=es,
            room=room_lh101,
            defaults={'spacing_rule': 'ALTERNATE_COLS', 'status': SeatingPlan.Status.GENERATED}
        )
        plan.allocations.all().delete()

        allocated_count = 0
        for seat, st in zip(usable_seats, eligible_students):
            SeatAllocation.objects.create(
                seating_plan=plan,
                seat=seat,
                student=st
            )
            allocated_count += 1

        plan.total_allocated = allocated_count
        plan.save()

    print(f"  [+] Seating plans generated for {len(eligible_students)} students across examination halls")

    # 10. Invigilation Allocation
    for idx, es in enumerate([es1, es2, es3, es5]):
        assigned_faculty = faculties[idx % len(faculties)]
        InvigilatorDuty.objects.get_or_create(
            exam_subject=es,
            room=room_lh101,
            defaults={
                'faculty': assigned_faculty,
                'duty_role': InvigilatorDuty.DutyRole.HALL_INVIGILATOR,
                'status': InvigilatorDuty.Status.CONFIRMED,
                'reporting_time': time(9, 0)
            }
        )
    print("  [+] Invigilator duties assigned & confirmed without faculty clashes")

    # 11. Hall Ticket Generation with Local ReportLab PDF
    print("  [*] Generating Official Hall Tickets and PDF documents...")
    ticket_count = 0
    for st in eligible_students:
        ticket_number = f"HT-{session.session_code}-{st.roll_no}"
        ticket, _ = HallTicket.objects.get_or_create(
            student=st,
            exam_session=session,
            defaults={'ticket_number': ticket_number}
        )
        ticket.entries.all().delete()

        for es in [es1, es2, es3, es5]:
            alloc = SeatAllocation.objects.filter(seating_plan__exam_subject=es, student=st).first()
            if alloc and es.planned_date:
                HallTicketEntry.objects.create(
                    hall_ticket=ticket,
                    exam_subject=es,
                    exam_date=es.planned_date,
                    time_slot_str=f"{es.time_slot.name} ({es.time_slot.start_time.strftime('%I:%M %p')})" if es.time_slot else "Morning",
                    room_number=alloc.seating_plan.room.room_number,
                    seat_label=alloc.seat.seat_label
                )

        # Generate ReportLab PDF
        pdf_bytes = generate_hall_ticket_pdf(ticket)
        ticket.pdf_file.save(f"{ticket.ticket_number}.pdf", ContentFile(pdf_bytes), save=True)
        ticket_count += 1

    print(f"  [+] {ticket_count} Hall Tickets with Local ReportLab PDFs generated")

    # 12. Examination Attendance Recording & Audits
    for es in [es1, es2]:
        sheet, _ = ExamAttendanceSheet.objects.get_or_create(
            exam_subject=es,
            room=room_lh101,
            defaults={
                'recorded_by': admin_user,
                'invigilator': faculties[0],
                'is_submitted': True,
                'submitted_at': django.utils.timezone.now()
            }
        )
        allocations = SeatAllocation.objects.filter(seating_plan__exam_subject=es, seating_plan__room=room_lh101)
        for idx, alloc in enumerate(allocations):
            # Mark 1 student absent, 1 late, rest present
            if idx == 5:
                stat = AttendanceRecord.Status.ABSENT
                booklet = ''
            elif idx == 12:
                stat = AttendanceRecord.Status.LATE
                booklet = f"BK-2026-{1000 + idx}"
            else:
                stat = AttendanceRecord.Status.PRESENT
                booklet = f"BK-2026-{1000 + idx}"

            rec, _ = AttendanceRecord.objects.get_or_create(
                sheet=sheet,
                student=alloc.student,
                defaults={
                    'seat_label': alloc.seat.seat_label,
                    'status': stat,
                    'answer_booklet_no': booklet,
                    'updated_by': admin_user
                }
            )

        sheet.total_students = sheet.records.count()
        sheet.present_count = sheet.records.filter(status='PRESENT').count()
        sheet.absent_count = sheet.records.filter(status='ABSENT').count()
        sheet.malpractice_count = 0
        sheet.save()

    print("  [+] Examination attendance recorded with booklet logs and correction audits")

    # 13. Institutional Announcements & In-App Notifications
    ann1, _ = Announcement.objects.get_or_create(
        title="Official Timetable Published - ESE May 2026",
        defaults={
            'content': 'The final, conflict-free timetable for End Semester Examinations May 2026 has been approved and published. Students can view room allocations and download Hall Tickets.',
            'target_role': Announcement.TargetRole.ALL,
            'priority': Announcement.Priority.HIGH,
            'published_by': admin_user
        }
    )
    ann2, _ = Announcement.objects.get_or_create(
        title="Hall Ticket Verification & Admit Card Guidelines",
        defaults={
            'content': 'All candidates must produce their printed Hall Ticket along with university identity cards. Entry is strictly barred without valid admit cards.',
            'target_role': Announcement.TargetRole.STUDENT,
            'priority': Announcement.Priority.URGENT,
            'published_by': admin_user
        }
    )
    ann3, _ = Announcement.objects.get_or_create(
        title="Invigilation Roster Notice for Faculty Members",
        defaults={
            'content': 'Duty assignments for May 2026 examinations have been uploaded. Faculty members are requested to confirm reporting times 30 minutes prior to session commencement.',
            'target_role': Announcement.TargetRole.FACULTY,
            'priority': Announcement.Priority.NORMAL,
            'published_by': admin_user
        }
    )

    # In-app notifications for admin and sample student
    InAppNotification.objects.get_or_create(
        user=admin_user,
        title="Examination Lifecycle Readiness: 100%",
        defaults={'message': 'All modules have completed phase validation. Timetables published, 23 hall tickets generated.', 'notification_type': 'SYSTEM'}
    )
    if eligible_students:
        st_user = eligible_students[0].user
        InAppNotification.objects.get_or_create(
            user=st_user,
            title="Hall Ticket Ready for Download",
            defaults={'message': 'Your hall ticket for ESE May 2026 is generated and ready for PDF download.', 'notification_type': 'HALL_TICKET'}
        )

    # 14. Audit Logs
    AuditLog.objects.create(
        user=admin_user,
        action=AuditLog.Action.PUBLISH,
        resource_type='TIMETABLE',
        resource_id=session.session_code,
        details={'subjects_scheduled': 4, 'clashes': 0, 'status': 'PUBLISHED'}
    )
    AuditLog.objects.create(
        user=admin_user,
        action=AuditLog.Action.GENERATE,
        resource_type='HALL_TICKETS',
        resource_id=session.session_code,
        details={'bulk_issued': ticket_count, 'format': 'ReportLab PDF'}
    )

    print("  [+] Announcements, notifications, and administrative audit trails recorded")
    print("[SUCCESS] ExamForge Database Seeding Successfully Completed!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed ExamForge demo data.')
    parser.add_argument(
        '--extended-students',
        action='store_true',
        help='Add 100 idempotent student records in academic year 2026-2027.',
    )
    args = parser.parse_args()
    if args.extended_students:
        run_extended_student_seed()
    else:
        run_seed()
