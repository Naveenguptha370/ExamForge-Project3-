"""
Exhaustive Faculty Management Test Suite
Member 1: Faculty Management
"""
from django.test import TestCase
from accounts.models import User
from faculty.models import FacultyProfile, FacultyAvailability, FacultyLeave
from faculty.profile_service import FacultyAccreditationService
from faculty.workload_engine import FacultyWorkloadCalculator

class ComprehensiveFacultyTestSuite(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='fac_comp_test', email='test@examforge.edu')
        self.profile = FacultyProfile.objects.create(
            user=self.user,
            faculty_id='FAC-COMP-01',
            department='Computer Science',
            designation='Professor',
            status='ACTIVE',
            email='test@examforge.edu',
            phone='9876543210'
        )

    def test_invigilation_eligibility(self):
        eval_res = FacultyAccreditationService.evaluate_invigilation_eligibility(self.profile)
        self.assertTrue(eval_res['is_eligible'])
        self.assertEqual(eval_res['duty_tier'], 'CHIEF_INVIGILATOR')

    def test_workload_metrics_calculation(self):
        metrics = FacultyWorkloadCalculator.calculate_workload_metrics('Computer Science')
        self.assertGreaterEqual(metrics['total_faculty_evaluated'], 1)
