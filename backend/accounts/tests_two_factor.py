"""
Unit tests for Member 1 TOTP and Backup Codes Engine.
"""
from django.test import TestCase
from accounts.two_factor import TOTPEngine, BackupCodeManager

class TwoFactorAuthenticationTests(TestCase):
    def test_totp_generation_and_verification(self):
        secret = TOTPEngine.generate_secret()
        self.assertGreater(len(secret), 16)

        otp = TOTPEngine.generate_otp(secret)
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

        is_valid = TOTPEngine.verify_otp(secret, otp)
        self.assertTrue(is_valid)

        invalid = TOTPEngine.verify_otp(secret, '000000' if otp != '000000' else '999999')
        self.assertFalse(invalid)

    def test_backup_codes_lifecycle(self):
        codes = BackupCodeManager.generate_backup_codes()
        self.assertEqual(len(codes), 8)

        code_to_use = codes[0]
        success, remaining = BackupCodeManager.verify_and_consume(code_to_use, codes)
        self.assertTrue(success)
        self.assertEqual(len(remaining), 7)
        self.assertNotIn(code_to_use, remaining)

        # Trying to consume again should fail
        fail, still_remaining = BackupCodeManager.verify_and_consume(code_to_use, remaining)
        self.assertFalse(fail)
        self.assertEqual(len(still_remaining), 7)
