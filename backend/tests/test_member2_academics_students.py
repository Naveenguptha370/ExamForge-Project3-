import csv
import io

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
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

    def _csv_upload(self, rows, headers=None, bom=False):
        headers = headers or [
            'registration_no',
            'roll_no',
            'first_name',
            'last_name',
            'email',
            'department_code',
            'course_code',
            'semester_number',
            'branch_code',
            'phone',
        ]
        content = io.StringIO(newline='')
        writer = csv.DictWriter(content, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                header: row.get(header.strip().lower().lstrip('\ufeff'), '')
                for header in headers
            })
        encoded = content.getvalue().encode('utf-8')
        if bom:
            encoded = b'\xef\xbb\xbf' + encoded
        return SimpleUploadedFile('students.csv', encoded, content_type='text/csv')

    def _valid_csv_row(self, **overrides):
        row = {
            'registration_no': 'REG-IMPORT-001',
            'roll_no': '24CS101',
            'first_name': 'Import',
            'last_name': 'Student',
            'email': 'import.student@test.edu',
            'department_code': 'CSE',
            'course_code': 'BTECH',
            'semester_number': '4',
            'branch_code': 'CSE-AI',
            'phone': '+91 90000 12345',
        }
        row.update(overrides)
        return row

    def test_csv_preview_accepts_utf8_bom_and_normalizes_headers(self):
        row = self._valid_csv_row()
        headers = [
            ' registration_no ',
            'roll_no',
            'first_name',
            'last_name',
            'email',
            'department_code',
            'course_code',
            'semester_number',
            'branch_code',
            'phone',
        ]
        upload = self._csv_upload([row], headers=headers, bom=True)

        response = self.client.post(
            '/api/students/profiles/csv_preview/',
            {'file': upload},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid_count'], 1)
        self.assertEqual(response.data['invalid_count'], 0)

    def test_csv_preview_reports_existing_and_in_file_duplicates(self):
        duplicate_existing = self._valid_csv_row(
            registration_no='reg-test-001',
            roll_no='24cs001',
            email='AARAV@TEST.EDU',
        )
        duplicate_in_file = self._valid_csv_row(
            registration_no='REG-IMPORT-002',
            roll_no='24CS102',
            email='duplicate@test.edu',
        )
        duplicate_in_file_again = self._valid_csv_row(
            registration_no='REG-IMPORT-003',
            roll_no='24cs102',
            email='DUPLICATE@test.edu',
        )

        response = self.client.post(
            '/api/students/profiles/csv_preview/',
            {'file': self._csv_upload([
                duplicate_existing,
                duplicate_in_file,
                duplicate_in_file_again,
            ])},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid_count'], 0)
        self.assertEqual(response.data['invalid_count'], 3)
        self.assertTrue(any('Registration number already exists' in error for error in response.data['errors']))
        self.assertTrue(any('Roll number is duplicated in this CSV' in error for error in response.data['errors']))
        self.assertTrue(any('Email is duplicated in this CSV' in error for error in response.data['errors']))

    def test_csv_import_rejects_invalid_batch_without_partial_writes(self):
        valid_row = self._valid_csv_row()
        duplicate_row = self._valid_csv_row(
            registration_no='REG-IMPORT-002',
            roll_no=self.student.roll_no,
            email='another.student@test.edu',
        )
        original_count = StudentProfile.objects.count()

        response = self.client.post(
            '/api/students/profiles/csv_import/',
            {'file': self._csv_upload([valid_row, duplicate_row])},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['created_count'], 0)
        self.assertEqual(StudentProfile.objects.count(), original_count)
        self.assertFalse(StudentProfile.objects.filter(registration_no='REG-IMPORT-001').exists())

    def test_csv_import_creates_valid_batch_and_rejects_reimport(self):
        row = self._valid_csv_row(
            registration_no=' reg-import-001 ',
            roll_no='24cs101',
            email='Import.Student@Test.edu',
        )
        response = self.client.post(
            '/api/students/profiles/csv_import/',
            {'file': self._csv_upload([row])},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['created_count'], 1)
        self.assertTrue(StudentProfile.objects.filter(
            registration_no='REG-IMPORT-001',
            roll_no='24CS101',
            email='import.student@test.edu',
        ).exists())

        duplicate_response = self.client.post(
            '/api/students/profiles/csv_import/',
            {'file': self._csv_upload([row])},
            format='multipart',
        )

        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(duplicate_response.data['created_count'], 0)
        self.assertEqual(StudentProfile.objects.filter(registration_no='REG-IMPORT-001').count(), 1)

    def test_csv_import_rejects_invalid_course_department_relationship(self):
        other_department = Department.objects.create(code='ECE', name='Electronics')
        self.course.department = other_department
        self.course.save(update_fields=['department'])
        original_count = StudentProfile.objects.count()

        response = self.client.post(
            '/api/students/profiles/csv_import/',
            {'file': self._csv_upload([self._valid_csv_row()])},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(any(
            'Course does not belong to the selected department' in error
            for error in response.data['errors']
        ))
        self.assertEqual(StudentProfile.objects.count(), original_count)

    def test_csv_preview_rejects_missing_headers(self):
        response = self.client.post(
            '/api/students/profiles/csv_preview/',
            {'file': self._csv_upload([{'registration_no': 'REG-IMPORT-001'}], headers=['registration_no'])},
            format='multipart',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Missing required columns', response.data['error'])
