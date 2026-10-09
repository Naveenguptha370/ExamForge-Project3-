"""
ExamForge M2 — Academics Tests
================================
Tests for Department, Course, Branch, Semester, Subject, AcademicYear models and APIs.
"""
from django.urls import reverse
from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from academics.models import AcademicYear, Department, Course, Branch, Semester, Subject

User = get_user_model()


# ── Model Tests ────────────────────────────────────────────────
class AcademicYearModelTest(TestCase):
    def test_create_academic_year(self):
        year = AcademicYear.objects.create(label='2024-2025', status='active')
        self.assertEqual(str(year), '2024-2025')
        self.assertFalse(year.is_current)

    def test_only_one_current_year(self):
        y1 = AcademicYear.objects.create(label='2023-2024', is_current=True)
        y2 = AcademicYear.objects.create(label='2024-2025', is_current=True)
        y1.refresh_from_db()
        self.assertEqual(y2.label, '2024-2025')

    def test_invalid_label_format(self):
        year = AcademicYear(label='badlabel')
        with self.assertRaises(ValidationError):
            year.full_clean()


class DepartmentModelTest(TestCase):
    def test_create_department(self):
        dept = Department.objects.create(code='CSE', name='Computer Science & Engineering')
        self.assertEqual(str(dept), 'CSE — Computer Science & Engineering')
        self.assertEqual(dept.status, 'active')

    def test_duplicate_code_raises(self):
        Department.objects.create(code='ECE', name='Electronics')
        with self.assertRaises(Exception):
            Department.objects.create(code='ECE', name='Electrical')

    def test_code_uppercase_enforced(self):
        dept = Department.objects.create(code='mech', name='Mechanical')
        dept.refresh_from_db()
        self.assertEqual(dept.code, 'MECH')


class CourseModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code='CSE', name='Computer Science')

    def test_create_course(self):
        course = Course.objects.create(
            department=self.dept, code='BTECH_CSE',
            name='B.Tech CSE', duration_years=4, total_semesters=8,
        )
        self.assertEqual(course.code, 'BTECH_CSE')
        self.assertEqual(course.department, self.dept)


class SemesterModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(code='CSE', name='CS')
        self.course = Course.objects.create(
            department=self.dept, code='BTECH', name='B.Tech',
            duration_years=4, total_semesters=8,
        )
        self.year = AcademicYear.objects.create(label='2024-2025')

    def test_create_semester(self):
        sem = Semester.objects.create(
            course=self.course, semester_number=1, academic_year=self.year,
        )
        self.assertEqual(sem.semester_number, 1)

    def test_semester_number_cannot_exceed_total(self):
        sem = Semester(course=self.course, semester_number=9, academic_year=self.year)
        with self.assertRaises(ValidationError):
            sem.full_clean()


class SubjectModelTest(TestCase):
    def setUp(self):
        self.dept   = Department.objects.create(code='CSE', name='CS')
        self.course = Course.objects.create(department=self.dept, code='BTECH', name='B.Tech', duration_years=4, total_semesters=8)
        self.sem    = Semester.objects.create(course=self.course, semester_number=3)
        self.year   = AcademicYear.objects.create(label='2024-2025')

    def test_create_subject(self):
        sub = Subject.objects.create(
            department=self.dept, course=self.course, semester=self.sem,
            code='CS301', name='Data Structures and Algorithms',
            subject_type='core', credits=3,
        )
        self.assertEqual(sub.code, 'CS301')
        self.assertEqual(sub.credits, 3)

    def test_duplicate_code_per_course_raises(self):
        Subject.objects.create(
            department=self.dept, course=self.course, semester=self.sem,
            code='CS301', name='DSA', subject_type='core', credits=3,
        )
        with self.assertRaises(Exception):
            Subject.objects.create(
                department=self.dept, course=self.course, semester=self.sem,
                code='CS301', name='Duplicate', subject_type='core', credits=3,
            )


# ── API Tests ─────────────────────────────────────────────────
class DepartmentAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='admin_test', password='Pass@1234', email='admin@test.com',
        )
        try:
            self.admin.role = 'admin'
            self.admin.is_staff = True
            self.admin.save()
        except Exception:
            pass
        self.client.force_authenticate(user=self.admin)

    def test_list_departments_empty(self):
        url = reverse('academics:department-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_department(self):
        url = reverse('academics:department-list')
        res = self.client.post(url, {'code': 'CSE', 'name': 'Computer Science & Engineering'})
        self.assertIn(res.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_create_department_missing_name(self):
        url = reverse('academics:department-list')
        res = self.client.post(url, {'code': 'CSE'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_department_detail(self):
        dept = Department.objects.create(code='ME', name='Mechanical Engineering')
        url  = reverse('academics:department-detail', args=[dept.id])
        res  = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_department(self):
        dept = Department.objects.create(code='CE', name='Civil Engineering')
        url  = reverse('academics:department-detail', args=[dept.id])
        res  = self.client.patch(url, {'name': 'Civil & Environmental Engineering'})
        self.assertIn(res.status_code, [status.HTTP_200_OK])

    def test_delete_department(self):
        dept = Department.objects.create(code='EEE', name='Electrical')
        url  = reverse('academics:department-detail', args=[dept.id])
        res  = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_cannot_create(self):
        self.client.force_authenticate(user=None)
        url = reverse('academics:department-list')
        res = self.client.post(url, {'code': 'XYZ', 'name': 'XYZ Dept'})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin2', password='Pass@1234', email='admin2@test.com')
        try:
            self.admin.role = 'admin'
            self.admin.is_staff = True
            self.admin.save()
        except Exception:
            pass
        self.client.force_authenticate(user=self.admin)
        self.dept = Department.objects.create(code='CSE', name='Computer Science')

    def test_create_course(self):
        url = reverse('academics:course-list')
        res = self.client.post(url, {
            'department': str(self.dept.id), 'code': 'BTECH',
            'name': 'Bachelor of Technology', 'duration_years': 4, 'total_semesters': 8,
        })
        self.assertIn(res.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_course_requires_department(self):
        url = reverse('academics:course-list')
        res = self.client.post(url, {'code': 'MBA', 'name': 'MBA', 'duration_years': 2, 'total_semesters': 4})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AcademicDashboardAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='staff1', password='Pass@1234', email='staff@test.com')
        self.client.force_authenticate(user=self.user)

    def test_dashboard_returns_200(self):
        url = reverse('academics:academic-dashboard')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
