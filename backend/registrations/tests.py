"""
ExamForge M2 — Registration Tests
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from academics.models import AcademicYear, Department, Course, Semester, Subject
from students.models import Student
from registrations.models import SubjectRegistration, ExamRegistration

User = get_user_model()


def make_admin():
    u = User.objects.create_user(username='reg_admin', password='Pass@1234', email='reg_admin@test.com')
    try:
        u.role = 'admin'
        u.is_staff = True
        u.save()
    except Exception:
        pass
    return u


def make_test_data():
    year   = AcademicYear.objects.create(label='2024-2025', is_current=True)
    dept   = Department.objects.create(code='RTST', name='Reg Test Dept')
    course = Course.objects.create(department=dept, code='RBTECH', name='Reg B.Tech', duration_years=4, total_semesters=8)
    sem    = Semester.objects.create(course=course, semester_number=3, academic_year=year)
    subject = Subject.objects.create(
        department=dept, course=course, semester=sem,
        code='RCS301', name='Reg Subject 1',
        subject_type='core', credits=3,
    )
    student = Student.objects.create(
        roll_number='RREG001', full_name='Reg Student',
        institutional_email='reg@test.edu',
        department=dept, course=course,
        current_semester=sem, academic_year=year,
        admission_year=2024, status='active',
        is_eligible_for_exam=True,
    )
    return year, dept, course, sem, subject, student


class SubjectRegistrationModelTest(TestCase):
    def setUp(self):
        self.year, self.dept, self.course, self.sem, self.subject, self.student = make_test_data()

    def test_create_subject_registration(self):
        reg = SubjectRegistration.objects.create(
            student=self.student, subject=self.subject, academic_year=self.year,
        )
        self.assertEqual(reg.status, 'registered')
        self.assertEqual(reg.student_roll, 'RREG001')
        self.assertEqual(reg.subject_code, 'RCS301')

    def test_cancel_registration(self):
        reg = SubjectRegistration.objects.create(
            student=self.student, subject=self.subject, academic_year=self.year,
        )
        reg.cancel(reason='Test cancellation')
        self.assertEqual(reg.status, 'cancelled')
        self.assertIsNotNone(reg.cancelled_at)
        self.assertFalse(reg.is_active)

    def test_ineligible_student_raises(self):
        self.student.is_eligible_for_exam = False
        self.student.save()
        reg = SubjectRegistration(
            student=self.student, subject=self.subject, academic_year=self.year,
        )
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            reg.clean()


class SubjectRegistrationAPITest(APITestCase):
    def setUp(self):
        self.admin = make_admin()
        self.client.force_authenticate(user=self.admin)
        self.year, self.dept, self.course, self.sem, self.subject, self.student = make_test_data()

    def test_create_registration(self):
        res = self.client.post(reverse('registrations:subject-registration-list'), {
            'student': str(self.student.id),
            'subject': str(self.subject.id),
            'academic_year': str(self.year.id),
        })
        self.assertIn(res.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_duplicate_registration_rejected(self):
        SubjectRegistration.objects.create(
            student=self.student, subject=self.subject, academic_year=self.year,
        )
        res = self.client.post(reverse('registrations:subject-registration-list'), {
            'student': str(self.student.id),
            'subject': str(self.subject.id),
            'academic_year': str(self.year.id),
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_registration(self):
        reg = SubjectRegistration.objects.create(
            student=self.student, subject=self.subject, academic_year=self.year,
        )
        url = reverse('registrations:subject-registration-cancel', args=[reg.id])
        res = self.client.post(url, {'reason': 'Test cancel'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_registrations(self):
        res = self.client.get(reverse('registrations:subject-registration-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_registration_dashboard(self):
        res = self.client.get(reverse('registrations:registration-dashboard'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_available_subjects_requires_student(self):
        res = self.client.get(reverse('registrations:registration-available-subjects'))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_available_subjects_for_valid_student(self):
        res = self.client.get(reverse('registrations:registration-available-subjects'), {'student': str(self.student.id)})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
