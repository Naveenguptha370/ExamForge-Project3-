"""
Unit tests for Member 1 Availability Slot Solver.
"""
from datetime import time
from django.test import TestCase
from accounts.models import User
from faculty.models import FacultyProfile, FacultyAvailability
from faculty.availability_engine import AvailabilitySlotSolver

class AvailabilityEngineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='prof_avail', email='avail@examforge.edu')
        self.faculty = FacultyProfile.objects.create(
            user=self.user, faculty_id='FAC-AV-01', department='Civil',
            designation='Professor', email='avail@examforge.edu'
        )

    def test_validate_slot_times(self):
        valid, _ = AvailabilitySlotSolver.validate_slot_times(time(9, 0), time(12, 0))
        self.assertTrue(valid)

        invalid_order, err = AvailabilitySlotSolver.validate_slot_times(time(12, 0), time(9, 0))
        self.assertFalse(invalid_order)
        self.assertIn("must precede", err)

        too_short, err = AvailabilitySlotSolver.validate_slot_times(time(9, 0), time(9, 15))
        self.assertFalse(too_short)
        self.assertIn("at least 30 minutes", err)

    def test_check_overlap(self):
        FacultyAvailability.objects.create(
            faculty=self.faculty, day_of_week='MONDAY',
            start_time=time(9, 0), end_time=time(12, 0), is_available=True
        )

        has_overlap = AvailabilitySlotSolver.check_overlap(
            self.faculty.id, 'MONDAY', time(10, 0), time(13, 0)
        )
        self.assertTrue(has_overlap)

        no_overlap = AvailabilitySlotSolver.check_overlap(
            self.faculty.id, 'MONDAY', time(13, 0), time(16, 0)
        )
        self.assertFalse(no_overlap)
