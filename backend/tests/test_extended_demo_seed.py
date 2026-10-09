from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.academics.models import Semester
from apps.registration.models import StudentEnrollment, SubjectRegistration
from apps.students.models import StudentProfile
from seed_demo_data import run_extended_student_seed


class ExtendedDemoStudentSeedTests(TestCase):
    def test_extended_seed_is_isolated_and_idempotent(self):
        run_extended_student_seed()
        run_extended_student_seed()

        students = StudentProfile.objects.filter(admission_year=2026)
        self.assertEqual(students.count(), 100)
        self.assertEqual(
            StudentEnrollment.objects.filter(
                student__in=students,
                academic_year='2026-2027',
            ).count(),
            100,
        )
        self.assertEqual(SubjectRegistration.objects.filter(student__in=students).count(), 400)
        self.assertEqual(
            SubjectRegistration.objects.filter(
                student__in=students,
                eligibility_status=SubjectRegistration.EligibilityStatus.ATTENDANCE_SHORTAGE,
            ).count(),
            5,
        )
        self.assertTrue(
            Semester.objects.filter(number=2, academic_year='2026-2027').exists()
        )
        self.assertEqual(
            get_user_model().objects.filter(username__startswith='student.26cs').count(),
            100,
        )
