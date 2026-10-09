"""
Unit tests for Member 1 User Lifecycle Manager.
"""
from django.test import TestCase
from accounts.models import User
from accounts.lifecycle_manager import UserLifecycleManager, UserLifecycleState

class UserLifecycleManagerTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin_lifecycle', role=User.Role.ADMIN, status=User.Status.ACTIVE)
        self.faculty = User.objects.create_user(username='faculty_user', role=User.Role.FACULTY, status=User.Status.ACTIVE)

    def test_valid_status_transition(self):
        ok, msg = UserLifecycleManager.transition_user(
            self.faculty,
            UserLifecycleState.INACTIVE,
            actor=self.admin,
            reason="Faculty sabbatical"
        )
        self.assertTrue(ok)
        self.faculty.refresh_from_db()
        self.assertEqual(self.faculty.status, UserLifecycleState.INACTIVE)
        self.assertFalse(self.faculty.is_active)

    def test_prevent_self_admin_deactivation(self):
        ok, msg = UserLifecycleManager.transition_user(
            self.admin,
            UserLifecycleState.INACTIVE,
            actor=self.admin,
            reason="Self-lock attempt"
        )
        self.assertFalse(ok)
        self.assertIn("cannot deactivate", msg)

    def test_disallowed_transition_from_archived(self):
        self.faculty.status = UserLifecycleState.ARCHIVED
        self.faculty.save()
        ok, msg = UserLifecycleManager.transition_user(
            self.faculty,
            UserLifecycleState.ACTIVE,
            actor=self.admin,
            reason="Archived reactivation"
        )
        self.assertFalse(ok)
        self.assertIn("disallowed", msg)
