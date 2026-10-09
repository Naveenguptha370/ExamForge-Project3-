"""
Exhaustive Authentication & Security Test Suite
Member 1: Authentication & User Management
"""
from django.test import TestCase
from accounts.models import User, AuditLog
from accounts.security_policies import PasswordComplexityEvaluator, AccountLockoutManager
from accounts.rbac import RoleCapabilityEngine, AcademicRole, GranularPermissions
from accounts.session_tracker import SessionSecurityManager
from accounts.two_factor import TOTPEngine, BackupCodeManager

class ComprehensiveAuthTestSuite(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='super_admin', role=User.Role.ADMIN)
        self.faculty = User.objects.create_user(username='prof_tester', role=User.Role.FACULTY)

    def test_rbac_admin_full_privileges(self):
        self.assertTrue(RoleCapabilityEngine.has_permission(AcademicRole.SUPER_ADMIN, GranularPermissions.USER_CREATE))
        self.assertTrue(RoleCapabilityEngine.has_permission(AcademicRole.SUPER_ADMIN, GranularPermissions.USER_DELETE))
        self.assertTrue(RoleCapabilityEngine.has_permission(AcademicRole.SUPER_ADMIN, GranularPermissions.AUDIT_VIEW))

    def test_rbac_faculty_restricted_privileges(self):
        self.assertFalse(RoleCapabilityEngine.has_permission(AcademicRole.FACULTY_INVIGILATOR, GranularPermissions.USER_CREATE))
        self.assertFalse(RoleCapabilityEngine.has_permission(AcademicRole.FACULTY_INVIGILATOR, GranularPermissions.USER_DELETE))
        self.assertTrue(RoleCapabilityEngine.has_permission(AcademicRole.FACULTY_INVIGILATOR, GranularPermissions.FACULTY_LEAVE_APPLY))

    def test_totp_cycle(self):
        secret = TOTPEngine.generate_secret()
        otp = TOTPEngine.generate_otp(secret)
        self.assertTrue(TOTPEngine.verify_otp(secret, otp))

    def test_session_concurrency(self):
        s1 = SessionSecurityManager.register_session(self.admin.id, 'Mozilla/5.0 (Windows NT 10.0)', '10.0.0.1')
        s2 = SessionSecurityManager.register_session(self.admin.id, 'Mozilla/5.0 (Macintosh)', '10.0.0.2')
        s3 = SessionSecurityManager.register_session(self.admin.id, 'Mozilla/5.0 (iPhone)', '10.0.0.3')
        sessions = SessionSecurityManager.get_user_sessions(self.admin.id)
        self.assertEqual(len(sessions), 3)

        # 4th session evicts the oldest
        s4 = SessionSecurityManager.register_session(self.admin.id, 'Mozilla/5.0 (Android)', '10.0.0.4')
        sessions_after = SessionSecurityManager.get_user_sessions(self.admin.id)
        self.assertEqual(len(sessions_after), 3)
