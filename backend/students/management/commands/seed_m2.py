"""ExamForge M2 — Seed Data Management Command
Creates demo departments, courses, semesters, subjects, and students for development.
"""
import datetime
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Seed ExamForge M2 with demo data for development.'

    @transaction.atomic
    def handle(self, *args, **options):
        from academics.models import AcademicYear, Department, Course, Branch, Semester, Subject

        self.stdout.write(self.style.MIGRATE_HEADING('[+] Seeding ExamForge M2 demo data...'))

        # Academic Year
        year, _ = AcademicYear.objects.get_or_create(
            label='2024-2025',
            defaults={
                'start_date': datetime.date(2024, 7, 1),
                'end_date': datetime.date(2025, 6, 30),
                'is_current': True,
                'status': 'active'
            },
        )
        self.stdout.write(f'  [OK] Academic Year: {year.label}')

        # Departments
        departments = [
            ('CSE', 'Computer Science & Engineering'),
            ('ECE', 'Electronics & Communication Engineering'),
            ('ME',  'Mechanical Engineering'),
            ('CE',  'Civil Engineering'),
        ]
        dept_objs = {}
        for code, name in departments:
            dept, _ = Department.objects.get_or_create(code=code, defaults={'name': name, 'status': 'active'})
            dept_objs[code] = dept
            self.stdout.write(f'  [OK] Dept: {code}')

        # Courses
        courses_data = [
            ('CSE', 'BTECH_CSE', 'B.Tech Computer Science', 4, 8),
            ('ECE', 'BTECH_ECE', 'B.Tech Electronics',     4, 8),
            ('ME',  'BTECH_ME',  'B.Tech Mechanical',       4, 8),
        ]
        course_objs = {}
        for dept_code, code, name, dur, sem_count in courses_data:
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={'department': dept_objs[dept_code], 'name': name, 'duration_years': dur, 'total_semesters': sem_count, 'status': 'active'},
            )
            course_objs[code] = course
            self.stdout.write(f'  [OK] Course: {code}')

        # Branches
        branches_data = [
            ('BTECH_CSE', 'CSE', 'Computer Science & Engineering', 60),
            ('BTECH_CSE', 'AI',  'Artificial Intelligence',        60),
            ('BTECH_ECE', 'ECE', 'Electronics & Communication',    60),
        ]
        branch_objs = {}
        for course_code, b_code, b_name, intake in branches_data:
            branch, _ = Branch.objects.get_or_create(
                code=b_code, course=course_objs[course_code],
                defaults={'name': b_name, 'intake_capacity': intake, 'status': 'active'},
            )
            branch_objs[b_code] = branch
            self.stdout.write(f'  [OK] Branch: {b_code}')

        # Semesters (1-8 for CSE)
        sem_objs = {}
        for i in range(1, 9):
            sem, _ = Semester.objects.get_or_create(
                course=course_objs['BTECH_CSE'],
                semester_number=i,
                defaults={'academic_year': year, 'status': 'active'},
            )
            sem_objs[i] = sem
        self.stdout.write('  [OK] Semesters: 1-8 for BTECH_CSE')

        # Subjects (Sem 3)
        subjects_seed = [
            ('CS301', 'Data Structures and Algorithms',      'core',     4, True),
            ('CS302', 'Operating Systems',                   'core',     3, True),
            ('CS303', 'Database Management Systems',         'core',     3, True),
            ('CS304', 'Computer Networks',                   'core',     3, True),
            ('CS305', 'DSA Lab',                             'lab',      1, False),
            ('CS306', 'DBMS Lab',                            'lab',      1, False),
            ('CS307', 'Discrete Mathematics',                'core',     3, True),
            ('CS308', 'Design and Analysis of Algorithms',   'core',     3, True),
        ]
        for code, name, stype, credits, is_ext in subjects_seed:
            sub, _ = Subject.objects.get_or_create(
                code=code,
                defaults={
                    'department': dept_objs['CSE'],
                    'course': course_objs['BTECH_CSE'],
                    'semester': sem_objs[3],
                    'name': name,
                    'subject_type': stype,
                    'credits': credits,
                    'is_external_exam': is_ext,
                    'status': 'active',
                },
            )
            self.stdout.write(f'  [OK] Subject: {code}')

        # Demo Students
        from students.models import Student
        students_seed = [
            ('CSE2024001', 'Aditya Kumar',   'aditya@college.edu',   dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[3], 2024),
            ('CSE2024002', 'Priya Sharma',   'priya@college.edu',    dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[3], 2024),
            ('CSE2024003', 'Rahul Singh',    'rahul@college.edu',    dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[3], 2024),
            ('CSE2024004', 'Deepika Nair',   'deepika@college.edu',  dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[3], 2024),
            ('CSE2024005', 'Arjun Patel',    'arjun@college.edu',    dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[3], 2024),
            ('CSE2024006', 'Sneha Reddy',    'sneha@college.edu',    dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[3], 2024),
            ('CSE2024007', 'Vikram Iyer',    'vikram@college.edu',   dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[5], 2022),
            ('CSE2024008', 'Lakshmi Das',    'lakshmi@college.edu',  dept_objs['CSE'], course_objs['BTECH_CSE'], sem_objs[7], 2021),
        ]
        for roll, name, email, dept, course, sem, adm_year in students_seed:
            st, created = Student.objects.get_or_create(
                roll_number=roll,
                defaults={
                    'student_id': f'STU-{roll}',
                    'full_name': name,
                    'institutional_email': email,
                    'department': dept,
                    'course': course,
                    'current_semester': sem,
                    'academic_year': year,
                    'admission_year': adm_year,
                    'status': 'active',
                    'is_eligible_for_exam': True,
                },
            )
            action = 'Created' if created else 'Exists'
            self.stdout.write(f'  [OK] Student [{action}]: {roll} - {name}')

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Seed data loaded successfully!'))
        self.stdout.write(self.style.NOTICE('   Visit http://localhost:8000/api/v1/ to explore the API.'))
        self.stdout.write(self.style.NOTICE('   Visit http://localhost:5173/ for the React frontend.'))
