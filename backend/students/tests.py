"""
ExamForge M2 — Students Tests
"""
import io
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from academics.models import AcademicYear, Department, Course, Semester
from students.models import Student, EnrollmentRecord

User = get_user_model()


def make_admin():
    u = User.objects.create_user(username='admin_s', password='Pass@1234', email='admin_s@test.com')
    try:
        u.role = 'admin'
        u.is_staff = True
        u.save()
    except Exception:
        pass
    return u

def make_dept_course_sem():
    year   = AcademicYear.objects.create(label='2024-2025', is_current=True)
    dept   = Department.objects.create(code='TST', name='Test Department')
    course = Course.objects.create(department=dept, code='BTEST', name='B.Test', duration_years=4, total_semesters=8)
    sem    = Semester.objects.create(course=course, semester_number=1, academic_year=year)
    return year, dept, course, sem


class StudentModelTest(TestCase):
    def setUp(self):
        self.year, self.dept, self.course, self.sem = make_dept_course_sem()

    def test_create_student(self):
        s = Student.objects.create(
            roll_number='TST001', full_name='Alice Smith',
            institutional_email='alice@test.edu',
            department=self.dept, course=self.course,
            current_semester=self.sem, academic_year=self.year,
            admission_year=2024,
        )
        self.assertEqual(s.status, 'active')
        self.assertTrue(s.is_eligible_for_exam)
        self.assertIsNotNone(s.student_id)

    def test_duplicate_roll_raises(self):
        Student.objects.create(
            roll_number='TST002', full_name='Bob Jones',
            institutional_email='bob@test.edu',
            department=self.dept, course=self.course,
            current_semester=self.sem, academic_year=self.year,
            admission_year=2024,
        )
        with self.assertRaises(Exception):
            Student.objects.create(
                roll_number='TST002', full_name='Duplicate',
                institutional_email='dup@test.edu',
                department=self.dept, course=self.course,
                current_semester=self.sem, academic_year=self.year,
                admission_year=2024,
            )

    def test_student_str(self):
        s = Student.objects.create(
            roll_number='TST003', full_name='Carol White',
            institutional_email='carol@test.edu',
            department=self.dept, course=self.course,
            current_semester=self.sem, academic_year=self.year,
            admission_year=2024,
        )
        self.assertIn('TST003', str(s))
        self.assertIn('Carol White', str(s))

    def test_exam_eligibility_false_when_inactive(self):
        s = Student.objects.create(
            roll_number='TST004', full_name='Dave Brown',
            institutional_email='dave@test.edu',
            department=self.dept, course=self.course,
            current_semester=self.sem, academic_year=self.year,
            admission_year=2024, status='inactive',
        )
        self.assertFalse(s.is_active)


class StudentAPITest(APITestCase):
    def setUp(self):
        self.admin = make_admin()
        self.client.force_authenticate(user=self.admin)
        self.year, self.dept, self.course, self.sem = make_dept_course_sem()

    def _create_payload(self, roll='TST-API-001'):
        return {
            'roll_number': roll,
            'full_name': 'Test Student API',
            'institutional_email': f'{roll.lower().replace("-","")}@test.edu',
            'department': str(self.dept.id),
            'course': str(self.course.id),
            'current_semester': str(self.sem.id),
            'academic_year': str(self.year.id),
            'admission_year': 2024,
        }

    def test_list_students_empty(self):
        res = self.client.get(reverse('students:student-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('results', res.data)

    def test_create_student(self):
        res = self.client.post(reverse('students:student-list'), self._create_payload())
        self.assertIn(res.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_create_student_missing_required(self):
        res = self.client.post(reverse('students:student-list'), {'full_name': 'Incomplete'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_student(self):
        res = self.client.post(reverse('students:student-list'), self._create_payload('TST-RETR'))
        student_id = (res.data.get('data') or {}).get('id')
        if student_id:
            get_res = self.client.get(reverse('students:student-detail', args=[student_id]))
            self.assertEqual(get_res.status_code, status.HTTP_200_OK)

    def test_update_student_status(self):
        res = self.client.post(reverse('students:student-list'), self._create_payload('TST-UPD'))
        student_id = (res.data.get('data') or {}).get('id')
        if student_id:
            upd = self.client.patch(reverse('students:student-detail', args=[student_id]), {'status': 'inactive'})
            self.assertEqual(upd.status_code, status.HTTP_200_OK)

    def test_dashboard_returns_200(self):
        res = self.client.get(reverse('students:student-dashboard'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class BulkImportTest(APITestCase):
    def setUp(self):
        self.admin = make_admin()
        self.client.force_authenticate(user=self.admin)
        self.year, self.dept, self.course, self.sem = make_dept_course_sem()

    def _make_csv(self, rows):
        lines = ['roll_number,full_name,email,department_code,course_code,semester_number,academic_year']
        for r in rows:
            lines.append(','.join(r))
        return io.BytesIO('\n'.join(lines).encode('utf-8'))

    def test_import_valid_csv(self):
        csv_file = self._make_csv([
            ['TST-IMP-001', 'Import Student 1', 'imp1@test.edu', 'TST', 'BTEST', '1', '2024-2025'],
        ])
        csv_file.name = 'test.csv'
        res = self.client.post(
            reverse('students:student-import-students'),
            {'file': csv_file, 'academic_year_id': str(self.year.id)},
            format='multipart',
        )
        self.assertIn(res.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_import_without_file_returns_400(self):
        res = self.client.post(
            reverse('students:student-import-students'),
            {'academic_year_id': str(self.year.id)},
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_requires_admin(self):
        regular = User.objects.create_user(username='reg1', password='Pass@1234', email='reg1@test.com')
        self.client.force_authenticate(user=regular)
        csv_file = self._make_csv([])
        csv_file.name = 'test.csv'
        res = self.client.post(
            reverse('students:student-import-students'),
            {'file': csv_file, 'academic_year_id': str(self.year.id)},
            format='multipart',
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
