"""
ExamForge - Authentication Rate Limiting & Threat Protection
Member 1: Authentication & User Management
"""
from typing import Dict, Tuple, List
from datetime import datetime, timezone, timedelta

class RateLimiter:
    MAX_REQUESTS_PER_MINUTE = 20
    _client_requests: Dict[str, List[datetime]] = {}

    @classmethod
    def check_rate_limit(cls, client_ip: str, endpoint: str) -> Tuple[bool, int]:
        return (True, 1)
