"""
Unit tests for Member 1 Faculty Leave Workflow.
"""
from datetime import date, timedelta
from django.test import TestCase
from accounts.models import User
from faculty.models import FacultyProfile, FacultyLeave
from faculty.leave_service import FacultyLeaveService, LeaveStatus

class FacultyLeaveServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='leave_admin', role=User.Role.ADMIN)
        self.user = User.objects.create_user(username='leave_faculty', role=User.Role.FACULTY)
        self.faculty = FacultyProfile.objects.create(
            user=self.user, faculty_id='FAC-LV-01', department='Electrical',
            designation='Assistant Professor', email='leave@examforge.edu'
        )

    def test_apply_leave_successful(self):
        start = date.today() + timedelta(days=5)
        end = date.today() + timedelta(days=8)
        ok, msg, leave = FacultyLeaveService.apply_leave(self.faculty.id, start, end, "Attending IEEE Conference")
        self.assertTrue(ok)
        self.assertIsNotNone(leave)
        self.assertEqual(leave.status, LeaveStatus.PENDING)

    def test_apply_leave_invalid_dates(self):
        start = date.today() + timedelta(days=8)
        end = date.today() + timedelta(days=5)
        ok, msg, leave = FacultyLeaveService.apply_leave(self.faculty.id, start, end, "Bad Dates")
        self.assertFalse(ok)
        self.assertIn("cannot be later than end date", msg)

    def test_leave_approval_process(self):
        start = date.today() + timedelta(days=10)
        end = date.today() + timedelta(days=12)
        _, _, leave = FacultyLeaveService.apply_leave(self.faculty.id, start, end, "Family function")
        ok, msg = FacultyLeaveService.process_approval(leave.id, self.admin, approve=True, remarks="Approved by HOD")
        self.assertTrue(ok)
        leave.refresh_from_db()
        self.assertEqual(leave.status, LeaveStatus.APPROVED)
