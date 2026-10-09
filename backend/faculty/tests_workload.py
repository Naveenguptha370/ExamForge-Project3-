"""
Unit tests for Member 1 Faculty Workload Calculator.
"""
from django.test import TestCase
from accounts.models import User
from faculty.models import FacultyProfile
from faculty.workload_engine import FacultyWorkloadCalculator

class WorkloadCalculatorTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='prof_w1', email='w1@examforge.edu')
        self.u2 = User.objects.create_user(username='asst_w2', email='w2@examforge.edu')
        self.p1 = FacultyProfile.objects.create(
            user=self.u1, faculty_id='FAC-WK-01', department='Mechanical',
            designation='Professor', status='ACTIVE', email='w1@examforge.edu'
        )
        self.p2 = FacultyProfile.objects.create(
            user=self.u2, faculty_id='FAC-WK-02', department='Mechanical',
            designation='Assistant Professor', status='ACTIVE', email='w2@examforge.edu'
        )

    def test_designation_target_duties(self):
        self.assertEqual(FacultyWorkloadCalculator.get_target_duties('Professor'), 3)
        self.assertEqual(FacultyWorkloadCalculator.get_target_duties('Associate Professor'), 5)
        self.assertEqual(FacultyWorkloadCalculator.get_target_duties('Assistant Professor'), 8)

    def test_calculate_workload_metrics(self):
        metrics = FacultyWorkloadCalculator.calculate_workload_metrics('Mechanical')
        self.assertEqual(metrics['total_faculty_evaluated'], 2)
        self.assertEqual(metrics['department_filter'], 'Mechanical')
