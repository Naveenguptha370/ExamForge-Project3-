"""
Unit tests for Member 1 Audit Trail Service.
"""
import json
from django.test import TestCase
from accounts.models import User, AuditLog
from accounts.audit_service import AuditTrailService

class AuditTrailServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username='audit_admin',
            email='audit@examforge.edu',
            role=User.Role.ADMIN
        )

    def test_calculate_diff(self):
        old_state = {'email': 'old@college.edu', 'role': 'FACULTY', 'phone': '1234567890'}
        new_state = {'email': 'new@college.edu', 'role': 'FACULTY', 'phone': '9876543210'}
        diff = AuditTrailService.calculate_diff(old_state, new_state)

        self.assertIn('email', diff)
        self.assertIn('phone', diff)
        self.assertNotIn('role', diff)
        self.assertEqual(diff['email']['before'], 'old@college.edu')
        self.assertEqual(diff['email']['after'], 'new@college.edu')

    def test_log_event_creation(self):
        diff = {'status': {'before': 'ACTIVE', 'after': 'INACTIVE'}}
        log = AuditTrailService.log_event(
            actor=self.admin,
            action='USER_DEACTIVATED',
            model_name='User',
            object_id='42',
            details='Account deactivated due to end of contract',
            diff=diff,
            ip_address='192.168.1.100'
        )

        self.assertIsNotNone(log.id)
        self.assertEqual(log.actor, self.admin)
        self.assertEqual(log.action, 'USER_DEACTIVATED')
        parsed = json.loads(log.details)
        self.assertEqual(parsed['message'], 'Account deactivated due to end of contract')
        self.assertIn('status', parsed['delta'])
