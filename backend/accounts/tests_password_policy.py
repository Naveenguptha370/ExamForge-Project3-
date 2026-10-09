"""
Unit tests for Member 1 password complexity and lockout engine.
"""
from django.test import TestCase
from accounts.security_policies import PasswordComplexityEvaluator, AccountLockoutManager

class PasswordSecurityPolicyTests(TestCase):
    def setUp(self):
        AccountLockoutManager.reset_lockout('prof_sharma')

    def test_minimum_length_requirement(self):
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('Short1!')
        self.assertFalse(valid)
        self.assertTrue(any("at least 10 characters" in e for e in errors))

    def test_strong_valid_password(self):
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('ExamForge#2026SecureAdmin')
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_account_lockout_after_failures(self):
        user = 'prof_sharma'
        for i in range(4):
            locked, count, mins = AccountLockoutManager.record_failed_attempt(user)
            self.assertFalse(locked)

        locked, count, mins = AccountLockoutManager.record_failed_attempt(user)
        self.assertTrue(locked)
        self.assertEqual(count, 5)
