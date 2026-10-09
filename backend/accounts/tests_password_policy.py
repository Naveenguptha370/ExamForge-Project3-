"""
Unit tests for Member 1 password complexity and lockout engine.
"""
from django.test import TestCase
from accounts.security_policies import (
    PasswordComplexityEvaluator,
    AccountLockoutManager,
    PasswordHistoryTracker
)

class PasswordSecurityPolicyTests(TestCase):
    def setUp(self):
        AccountLockoutManager.reset_lockout('prof_sharma')
        AccountLockoutManager.reset_lockout('exam_admin')

    def test_minimum_length_requirement(self):
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('Short1!')
        self.assertFalse(valid)
        self.assertTrue(any("at least 10 characters" in e for e in errors))

    def test_character_class_requirements(self):
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('alllowercase123!')
        self.assertFalse(valid)
        self.assertTrue(any("uppercase" in e for e in errors))

        valid, errors = PasswordComplexityEvaluator.validate_password_strength('ALLUPPERCASE123!')
        self.assertFalse(valid)
        self.assertTrue(any("lowercase" in e for e in errors))

        valid, errors = PasswordComplexityEvaluator.validate_password_strength('NoDigitsHereSpecial!')
        self.assertFalse(valid)
        self.assertTrue(any("numeric" in e for e in errors))

        valid, errors = PasswordComplexityEvaluator.validate_password_strength('NoSpecialChar1234')
        self.assertFalse(valid)
        self.assertTrue(any("special" in e for e in errors))

    def test_strong_valid_password(self):
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('ExamForge#2026SecureAdmin')
        self.assertTrue(valid)
        self.assertEqual(len(errors), 0)

    def test_common_weak_password_rejection(self):
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('password@123')
        self.assertFalse(valid)
        self.assertTrue(any("too common" in e for e in errors))

    def test_user_attribute_matching(self):
        attrs = {'username': 'sharma', 'email': 'sharma@college.edu'}
        valid, errors = PasswordComplexityEvaluator.validate_password_strength('MySharmaPass#2026', user_attributes=attrs)
        self.assertFalse(valid)
        self.assertTrue(any("username" in e for e in errors))

    def test_account_lockout_after_failures(self):
        user = 'prof_sharma'
        for i in range(4):
            locked, count, mins = AccountLockoutManager.record_failed_attempt(user)
            self.assertFalse(locked)
            self.assertEqual(count, i + 1)

        locked, count, mins = AccountLockoutManager.record_failed_attempt(user)
        self.assertTrue(locked)
        self.assertEqual(count, 5)
        self.assertEqual(mins, 30)

        is_l, rem_mins = AccountLockoutManager.is_locked(user)
        self.assertTrue(is_l)
        self.assertGreater(rem_mins, 0)

        AccountLockoutManager.reset_lockout(user)
        is_l, _ = AccountLockoutManager.is_locked(user)
        self.assertFalse(is_l)

    def test_password_history_prevent_reuse(self):
        old_pass = "OldPass#2025Alpha"
        old_hash = PasswordHistoryTracker.hash_password(old_pass)
        history = [old_hash, "another_dummy_hash"]
        self.assertTrue(PasswordHistoryTracker.check_history(old_pass, history))
        self.assertFalse(PasswordHistoryTracker.check_history("BrandNew#Pass2026", history))
