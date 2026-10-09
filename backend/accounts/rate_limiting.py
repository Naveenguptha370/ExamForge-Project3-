"""
ExamForge - Authentication Rate Limiting & Threat Protection
Member 1: Authentication & User Management
"""
from typing import Dict, Tuple, List
from datetime import datetime, timezone, timedelta

class RateLimiter:
    """Enforces sliding-window request throttling on sensitive authentication endpoints."""
    MAX_REQUESTS_PER_MINUTE = 20
    _client_requests: Dict[str, List[datetime]] = {}

    @classmethod
    def check_rate_limit(cls, client_ip: str, endpoint: str) -> Tuple[bool, int]:
        key = f"{client_ip}:{endpoint}"
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(minutes=1)

        if key not in cls._client_requests:
            cls._client_requests[key] = []

        cls._client_requests[key] = [t for t in cls._client_requests[key] if t > window_start]
        current_count = len(cls._client_requests[key])

        if current_count >= cls.MAX_REQUESTS_PER_MINUTE:
            return (False, current_count)

        cls._client_requests[key].append(now)
        return (True, current_count + 1)
