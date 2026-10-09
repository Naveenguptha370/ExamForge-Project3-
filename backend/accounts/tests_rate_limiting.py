"""
Unit tests for Member 1 Rate Limiter.
"""
from django.test import TestCase
from accounts.rate_limiting import RateLimiter

class RateLimiterTests(TestCase):
    def test_rate_limit_enforcement(self):
        ip = "192.168.1.55"
        endpoint = "/api/auth/login/"

        # Send up to limit
        for i in range(20):
            allowed, count = RateLimiter.check_rate_limit(ip, endpoint)
            self.assertTrue(allowed)

        # 21st should fail
        allowed, count = RateLimiter.check_rate_limit(ip, endpoint)
        self.assertFalse(allowed)
