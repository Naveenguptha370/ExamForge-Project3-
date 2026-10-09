from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, time, timedelta

from accounts.models import User
from academics.models import Department, Course, Subject, Faculty, FacultyLeave, Student
from infrastructure.models import Building, Room, RoomMaintenance, RoomAssignment
from infrastructure.services import ensure_room_seats
from examinations.models import ExamSession, TimeSlot, Examination, ExamRegistration
from seating.models import SeatingPlan, Seat, SeatAllocation
from seating.engine import SeatingEngine
from invigilation.models import InvigilatorDuty, DutyRequirement
from invigilation.engine import InvigilatorAllocationEngine


class Command(BaseCommand):
    help = "Seeds comprehensive, realistic institutional data for ExamForge"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting ExamForge institutional data seeding..."))

        # 1. Admin User
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@examforge.edu',
                'first_name': 'Chief',
                'last_name': 'Controller of Examinations',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('Admin@123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user: admin / Admin@123"))

        # 2. Departments
        dept_data = [
            ('CSE', 'Computer Science & Engineering', 'ARYA'),
            ('ECE', 'Electronics & Communication Engineering', 'RAMA'),
            ('MECH', 'Mechanical Engineering', 'VISV'),
            ('IT', 'Information Technology', 'ARYA'),
        ]
        depts = {}
        for code, name, bcode in dept_data:
            d, _ = Department.objects.get_or_create(code=code, defaults={'name': name, 'building_code': bcode})
            depts[code] = d

        # 3. Courses
        courses = {}
        courses['BTECH-CS'], _ = Course.objects.get_or_create(code='BTECH-CS', defaults={'name': 'B.Tech Computer Science & Eng.', 'department': depts['CSE']})
        courses['BTECH-EC'], _ = Course.objects.get_or_create(code='BTECH-EC', defaults={'name': 'B.Tech Electronics & Comm. Eng.', 'department': depts['ECE']})
        courses['BTECH-ME'], _ = Course.objects.get_or_create(code='BTECH-ME', defaults={'name': 'B.Tech Mechanical Engineering', 'department': depts['MECH']})

        # 4. Subjects
        subjects = {}
        sub_list = [
            ('CS401', 'Design & Analysis of Algorithms', depts['CSE'], 4, 4),
            ('CS402', 'Database Management Systems', depts['CSE'], 4, 3),
            ('EC401', 'Microprocessors & Microcontrollers', depts['ECE'], 4, 4),
            ('EC402', 'Digital Signal Processing', depts['ECE'], 4, 3),
            ('ME401', 'Heat & Mass Transfer', depts['MECH'], 4, 4),
            ('ME402', 'Fluid Mechanics & Turbomachinery', depts['MECH'], 4, 3),
        ]
        for code, name, dept, sem, cr in sub_list:
            s, _ = Subject.objects.get_or_create(code=code, defaults={'name': name, 'department': dept, 'semester': sem, 'credits': cr})
            subjects[code] = s

        # 5. Buildings
        buildings = {}
        b_list = [
            ('ARYA', 'Aryabhata Science Block', 'North Campus', 4, True),
            ('RAMA', 'Ramanujan Engineering Hall', 'East Campus', 3, True),
            ('VISV', 'Visvesvaraya Central Complex', 'Central Campus', 5, True),
        ]
        for code, name, zone, floors, elev in b_list:
            b, _ = Building.objects.get_or_create(code=code, defaults={'name': name, 'campus_zone': zone, 'total_floors': floors, 'has_elevator': elev})
            buildings[code] = b

        # 6. Examination Rooms
        room_list = [
            (buildings['ARYA'], 'A-101', 1, 'exam_hall', 36, 30, 6, 6, True, True, True, 'Equipped with 4K CCTV and digital clock'),
            (buildings['ARYA'], 'A-102', 1, 'lecture_hall', 30, 24, 6, 5, True, True, False, 'Standard examination hall with amphitheater tiers'),
            (buildings['ARYA'], 'A-201', 2, 'exam_hall', 36, 30, 6, 6, False, True, True, 'Air-conditioned main hall on second floor'),
            (buildings['RAMA'], 'R-101', 1, 'exam_hall', 40, 32, 8, 5, True, True, True, 'Ground floor accessible hall with wide aisles'),
            (buildings['RAMA'], 'R-202', 2, 'computer_lab', 25, 20, 5, 5, False, True, True, 'Computer lab with partitioned desks'),
            (buildings['RAMA'], 'R-301', 3, 'seminar_hall', 24, 20, 4, 6, False, False, True, 'Executive seminar hall'),
            (buildings['VISV'], 'V-AUD1', 0, 'exam_hall', 60, 48, 8, 6, True, True, True, 'Main central auditorium with acoustic panels'),
            (buildings['VISV'], 'V-201', 2, 'exam_hall', 30, 24, 5, 6, True, True, False, 'Spacious examination room overlooking central quad'),
        ]
        rooms = {}
        for b, num, fl, rtype, cap, u_cap, rows, cols, acc, cctv, ac, notes in room_list:
            r, _ = Room.objects.get_or_create(
                building=b,
                room_number=num,
                defaults={
                    'floor': fl,
                    'room_type': rtype,
                    'capacity': cap,
                    'usable_capacity': u_cap,
                    'rows': rows,
                    'columns': cols,
                    'is_accessible': acc,
                    'has_cctv': cctv,
                    'has_air_conditioning': ac,
                    'notes': notes
                }
            )
            ensure_room_seats(r)
            rooms[num] = r

        # 7. Room Maintenance
        RoomMaintenance.objects.get_or_create(
            room=rooms['R-301'],
            start_date=date(2026, 10, 10),
            end_date=date(2026, 10, 20),
            defaults={
                'reason': 'Acoustic ceiling repair and lighting upgrade',
                'is_resolved': False
            }
        )

        # 8. Faculty Members
        faculty_data = [
            ('FAC001', 'Dr. Arvind Sharma', 'arvind.sharma@examforge.edu', '9876543201', depts['CSE'], 'Professor', 5),
            ('FAC002', 'Prof. Sunita Rao', 'sunita.rao@examforge.edu', '9876543202', depts['CSE'], 'Associate Professor', 5),
            ('FAC003', 'Dr. Rajesh Nair', 'rajesh.nair@examforge.edu', '9876543203', depts['CSE'], 'Assistant Professor', 6),
            ('FAC004', 'Prof. Priya Menon', 'priya.menon@examforge.edu', '9876543204', depts['CSE'], 'Assistant Professor', 6),
            ('FAC005', 'Dr. Vikram Kulkarni', 'vikram.k@examforge.edu', '9876543205', depts['ECE'], 'Professor', 5),
            ('FAC006', 'Prof. Meenakshi Sundaram', 'meenakshi.s@examforge.edu', '9876543206', depts['ECE'], 'Associate Professor', 5),
            ('FAC007', 'Dr. Sanjay Patel', 'sanjay.patel@examforge.edu', '9876543207', depts['ECE'], 'Assistant Professor', 6),
            ('FAC008', 'Prof. Kavita Reddy', 'kavita.reddy@examforge.edu', '9876543208', depts['ECE'], 'Assistant Professor', 6),
            ('FAC009', 'Dr. Harish Joshi', 'harish.joshi@examforge.edu', '9876543209', depts['MECH'], 'Professor', 5),
            ('FAC010', 'Prof. Deepa Verma', 'deepa.verma@examforge.edu', '9876543210', depts['MECH'], 'Associate Professor', 5),
            ('FAC011', 'Dr. Rohan Deshmukh', 'rohan.d@examforge.edu', '9876543211', depts['MECH'], 'Assistant Professor', 6),
            ('FAC012', 'Prof. Ananya Gupta', 'ananya.gupta@examforge.edu', '9876543212', depts['IT'], 'Assistant Professor', 6),
        ]
        faculty_objs = {}
        for emp_id, name, email, phone, dept, desig, max_d in faculty_data:
            f, _ = Faculty.objects.get_or_create(
                employee_id=emp_id,
                defaults={
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'department': dept,
                    'designation': desig,
                    'max_weekly_duties': max_d,
                    'is_active': True
                }
            )
            faculty_objs[emp_id] = f

        # Faculty Leave
        FacultyLeave.objects.get_or_create(
            faculty=faculty_objs['FAC004'],
            start_date=date(2026, 10, 14),
            end_date=date(2026, 10, 17),
            defaults={'reason': 'Attending IEEE International Conference', 'is_approved': True}
        )

        # 9. Students
        # Generate 45 students (15 CSE, 15 ECE, 15 MECH)
        student_names = [
            ("Aarav Mehta", "CSE"), ("Aditi Singhania", "CSE"), ("Akash Varma", "CSE"),
            ("Ananya Pillai", "CSE"), ("Bhavya Nair", "CSE"), ("Chetan Bhat", "CSE"),
            ("Divya Hegde", "CSE"), ("Eshan Iyer", "CSE"), ("Farhan Qureshi", "CSE"),
            ("Gautam Sethi", "CSE"), ("Harini Rao", "CSE"), ("Ishaan Sen", "CSE"),
            ("Jaya Mathur", "CSE"), ("Karan Oberoi", "CSE"), ("Lavanya Joshi", "CSE"),

            ("Manish Tiwari", "ECE"), ("Neha Kapoor", "ECE"), ("Omkar Deshpande", "ECE"),
            ("Pooja Choudhury", "ECE"), ("Pranav Mukherjee", "ECE"), ("Raghav Swaminathan", "ECE"),
            ("Rhea D'Souza", "ECE"), ("Rohit Saxena", "ECE"), ("Sahil Bhattacharya", "ECE"),
            ("Sanya Malhotra", "ECE"), ("Shashank Dubey", "ECE"), ("Sneha Chawla", "ECE"),
            ("Tanvi Agarwal", "ECE"), ("Uday Kirloskar", "ECE"), ("Varun Chandra", "ECE"),

            ("Abhinav Kaul", "MECH"), ("Alok Tripathi", "MECH"), ("Ankit Pandey", "MECH"),
            ("Bharat Natarajan", "MECH"), ("Chirag Rathi", "MECH"), ("Darshan Kadam", "MECH"),
            ("Girish Nambiar", "MECH"), ("Kartik Somani", "MECH"), ("Manoj Somayaji", "MECH"),
            ("Nikhil Salvi", "MECH"), ("Pawan Mittal", "MECH"), ("Rajat Khandelwal", "MECH"),
            ("Sachin Tendolkar", "MECH"), ("Tarun Jagtiani", "MECH"), ("Yashaswi Patil", "MECH"),
        ]

        students = []
        for idx, (sname, dcode) in enumerate(student_names, start=1):
            dept = depts[dcode]
            course = courses[f"BTECH-{dcode[:2]}"]
            reg_no = f"REG2024{idx:03d}"
            roll_no = f"{dcode}24-{idx:03d}"
            s, _ = Student.objects.get_or_create(
                registration_no=reg_no,
                defaults={
                    'roll_no': roll_no,
                    'name': sname,
                    'email': f"{sname.lower().replace(' ', '.')}@student.examforge.edu",
                    'department': dept,
                    'course': course,
                    'semester': 4,
                    'is_eligible_for_exam': True
                }
            )
            students.append(s)

        # 10. Exam Session & Time Slots
        session, _ = ExamSession.objects.get_or_create(
            name='Spring End-Semester Examinations 2026',
            defaults={
                'academic_year': '2025-2026',
                'term': 'even',
                'start_date': date(2026, 10, 15),
                'end_date': date(2026, 10, 25),
                'status': 'published'
            }
        )

        slot_morning, _ = TimeSlot.objects.get_or_create(
            name='Morning Slot (09:30 AM - 12:30 PM)',
            defaults={'start_time': time(9, 30), 'end_time': time(12, 30)}
        )
        slot_afternoon, _ = TimeSlot.objects.get_or_create(
            name='Afternoon Slot (02:00 PM - 05:00 PM)',
            defaults={'start_time': time(14, 0), 'end_time': time(17, 0)}
        )

        # 11. Examinations
        exam1, _ = Examination.objects.get_or_create(
            session=session,
            subject=subjects['CS401'],
            defaults={
                'exam_date': date(2026, 10, 15),
                'time_slot': slot_morning,
                'duration_minutes': 180,
                'status': 'scheduled'
            }
        )

        exam2, _ = Examination.objects.get_or_create(
            session=session,
            subject=subjects['EC401'],
            defaults={
                'exam_date': date(2026, 10, 15),
                'time_slot': slot_morning,
                'duration_minutes': 180,
                'status': 'scheduled'
            }
        )

        exam3, _ = Examination.objects.get_or_create(
            session=session,
            subject=subjects['ME401'],
            defaults={
                'exam_date': date(2026, 10, 16),
                'time_slot': slot_morning,
                'duration_minutes': 180,
                'status': 'scheduled'
            }
        )

        # Register students for Exam 1 (all 45 students across 3 departments)
        for s in students:
            ExamRegistration.objects.get_or_create(examination=exam1, student=s, defaults={'is_eligible': True})

        # Register MECH students for Exam 3
        mech_students = [s for s in students if s.department.code == 'MECH']
        for s in mech_students:
            ExamRegistration.objects.get_or_create(examination=exam3, student=s, defaults={'is_eligible': True})

        # 12. Run Seating Engine for Exam 1 across A-101 and A-102
        self.stdout.write("Running automatic seating plan generation for Exam 1...")
        seating_result = SeatingEngine.generate(
            examination_id=exam1.id,
            room_ids=[rooms['A-101'].id, rooms['A-102'].id],
            spacing_rule='department_separated'
        )
        self.stdout.write(self.style.SUCCESS(f"Seating Plan generated: {seating_result['total_allocated']} students allocated!"))

        # 13. Run Invigilator Allocation Engine for Exam 1
        self.stdout.write("Running automatic invigilator allocation for Exam 1...")
        invig_result = InvigilatorAllocationEngine.allocate(
            examination_id=exam1.id,
            ratio_per_students=25,
            balance_workload=True
        )
        self.stdout.write(self.style.SUCCESS(f"Invigilators assigned: {invig_result['total_assigned']} duties created!"))

        self.stdout.write(self.style.SUCCESS("Institutional seed data generated successfully!"))
