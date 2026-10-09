"""
ExamForge - Authentication & Password Security Policies
Member 1: Authentication, User Management, and Faculty Management
"""
import re
import math
import hashlib
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime, timezone, timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordComplexityEvaluator:
    """
    Evaluates password strength and compliance with institutional standards.
    Strict NIST SP 800-63B guidelines and university compliance.
    """
    MIN_LENGTH = 10
    MAX_LENGTH = 128
    MIN_ENTROPY_BITS = 45.0

    COMMON_WEAK_PASSWORDS = {
        'password', 'password123', 'admin123', 'examforge', 'examforge2026',
        'college123', 'university', 'faculty123', 'welcome123', 'letmein123',
        'qwerty123', 'changeit', 'password@123', 'admin@123', 'exam@123'
    }

    @classmethod
    def calculate_entropy(cls, password: str) -> float:
        """Calculates Shannon entropy in bits for character diversity."""
        if not password:
            return 0.0
        pool_size = 0
        if re.search(r'[a-z]', password):
            pool_size += 26
        if re.search(r'[A-Z]', password):
            pool_size += 26
        if re.search(r'[0-9]', password):
            pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            pool_size += 33
        if pool_size == 0:
            return 0.0
        return len(password) * math.log2(pool_size)

    @classmethod
    def validate_password_strength(cls, password: str, user_attributes: Optional[Dict[str, str]] = None) -> Tuple[bool, List[str]]:
        errors = []
        if len(password) < cls.MIN_LENGTH:
            errors.append(f"Password must contain at least {cls.MIN_LENGTH} characters.")
        if len(password) > cls.MAX_LENGTH:
            errors.append(f"Password must not exceed {cls.MAX_LENGTH} characters.")
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter (A-Z).")
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter (a-z).")
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one numeric digit (0-9).")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?]', password):
            errors.append("Password must contain at least one special character.")

        if password.lower() in cls.COMMON_WEAK_PASSWORDS:
            errors.append("The password chosen is too common and easily guessable.")

        entropy = cls.calculate_entropy(password)
        if entropy < cls.MIN_ENTROPY_BITS:
            errors.append(f"Password entropy ({entropy:.1f} bits) is below the institutional threshold ({cls.MIN_ENTROPY_BITS} bits).")

        if user_attributes:
            for field, val in user_attributes.items():
                if val and len(val) >= 3 and val.lower() in password.lower():
                    errors.append(f"Password must not contain parts of user {field} ('{val}').")

        return (len(errors) == 0, errors)

class AccountLockoutManager:
    """
    Manages temporary and permanent account lockouts upon repeated invalid credentials.
    Protects examination portal from credential stuffing attacks.
    """
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30
    ATTEMPT_WINDOW_MINUTES = 15

    _failed_attempts: Dict[str, List[datetime]] = {}
    _locked_accounts: Dict[str, datetime] = {}

    @classmethod
    def record_failed_attempt(cls, username: str, ip_address: str = '') -> Tuple[bool, int, Optional[int]]:
        now = datetime.now(timezone.utc)
        clean_user = username.strip().lower()
        if clean_user not in cls._failed_attempts:
            cls._failed_attempts[clean_user] = []

        window_start = now - timedelta(minutes=cls.ATTEMPT_WINDOW_MINUTES)
        cls._failed_attempts[clean_user] = [
            ts for ts in cls._failed_attempts[clean_user] if ts > window_start
        ]
        cls._failed_attempts[clean_user].append(now)

        failures = len(cls._failed_attempts[clean_user])
        if failures >= cls.MAX_FAILED_ATTEMPTS:
            lockout_expiry = now + timedelta(minutes=cls.LOCKOUT_DURATION_MINUTES)
            cls._locked_accounts[clean_user] = lockout_expiry
            return (True, failures, cls.LOCKOUT_DURATION_MINUTES)

        return (False, failures, None)

    @classmethod
    def is_locked(cls, username: str) -> Tuple[bool, Optional[int]]:
        clean_user = username.strip().lower()
        now = datetime.now(timezone.utc)
        if clean_user in cls._locked_accounts:
            expiry = cls._locked_accounts[clean_user]
            if now < expiry:
                remaining_seconds = int((expiry - now).total_seconds())
                remaining_minutes = max(1, (remaining_seconds + 59) // 60)
                return (True, remaining_minutes)
            else:
                del cls._locked_accounts[clean_user]
                if clean_user in cls._failed_attempts:
                    cls._failed_attempts[clean_user] = []
        return (False, None)

    @classmethod
    def reset_lockout(cls, username: str) -> None:
        clean_user = username.strip().lower()
        cls._failed_attempts.pop(clean_user, None)
        cls._locked_accounts.pop(clean_user, None)

class PasswordHistoryTracker:
    """Maintains salted cryptographic hashes of historical passwords to prevent reuse."""
    HISTORY_DEPTH = 5

    @staticmethod
    def hash_password(password: str, salt: str = "examforge_salt") -> str:
        return hashlib.sha256(f"{salt}:{password}".encode('utf-8')).hexdigest()

    @classmethod
    def check_history(cls, new_password: str, historical_hashes: List[str]) -> bool:
        new_hash = cls.hash_password(new_password)
        return new_hash in historical_hashes
