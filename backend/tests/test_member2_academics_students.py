from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.academics.models import Department, Course, Branch, Semester, Subject
from apps.students.models import StudentProfile
from apps.registration.models import StudentEnrollment, SubjectRegistration

User = get_user_model()

class Member2AcademicsStudentsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin_m2', password='Password123!', role=User.Role.ADMIN)
        self.client.force_authenticate(user=self.admin)

        self.dept = Department.objects.create(code='CSE', name='Computer Science')
        self.course = Course.objects.create(code='BTECH', name='B.Tech', department=self.dept)
        self.branch = Branch.objects.create(code='CSE-AI', name='AI & ML', course=self.course)
        self.sem = Semester.objects.create(number=4, academic_year='2025-2026', term=Semester.Term.EVEN)

        self.subject = Subject.objects.create(
            code='CS401',
            name='Algorithms',
            department=self.dept,
            branch=self.branch,
            semester=self.sem,
            min_attendance_pct=75
        )

        self.student = StudentProfile.objects.create(
            registration_no='REG-TEST-001',
            roll_no='24CS001',
            first_name='Aarav',
            last_name='Kumar',
            email='aarav@test.edu',
            department=self.dept,
            course=self.course,
            branch=self.branch,
            semester=self.sem,
            is_eligible_for_exam=True
        )

    def test_student_unique_registration_and_roll_enforcement(self):
        with self.assertRaises(Exception):
            StudentProfile.objects.create(
                registration_no='REG-TEST-001',  # Duplicate reg
                roll_no='24CS002',
                first_name='Duplicate',
                last_name='User',
                email='dup1@test.edu',
                department=self.dept,
                course=self.course,
                semester=self.sem
            )

    def test_subject_registration_and_attendance_shortage_computation(self):
        # Register student with 60% attendance (below min 75%)
        reg = SubjectRegistration.objects.create(
            student=self.student,
            subject=self.subject,
            semester=self.sem,
            attendance_percentage=60.0
        )
        self.assertEqual(reg.eligibility_status, SubjectRegistration.EligibilityStatus.ATTENDANCE_SHORTAGE)
        self.assertFalse(reg.is_eligible())

    def test_duplicate_subject_registration_rejected(self):
        SubjectRegistration.objects.create(
            student=self.student,
            subject=self.subject,
            semester=self.sem,
            attendance_percentage=85.0
        )
        with self.assertRaises(Exception):
            SubjectRegistration.objects.create(
                student=self.student,
                subject=self.subject,
                semester=self.sem
            )
