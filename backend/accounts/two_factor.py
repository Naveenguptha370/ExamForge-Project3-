"""
ExamForge - Two-Factor Authentication (TOTP) & Backup Codes Engine
Member 1: Authentication & User Management
"""
import hmac
import hashlib
import time
import base64
import os
from typing import List, Tuple, Optional

class TOTPEngine:
    """Implements RFC 6238 Time-Based One-Time Password algorithm."""
    TIME_STEP = 30
    DIGITS = 6

    @classmethod
    def generate_secret(cls) -> str:
        random_bytes = os.urandom(20)
        return base64.b32encode(random_bytes).decode('utf-8')

    @classmethod
    def generate_otp(cls, secret: str, timestamp: Optional[int] = None) -> str:
        if timestamp is None:
            timestamp = int(time.time())
        time_counter = int(timestamp // cls.TIME_STEP)
        counter_bytes = time_counter.to_bytes(8, byteorder='big')

        # Decode base32 secret
        padding = '=' * ((8 - len(secret) % 8) % 8)
        secret_bytes = base64.b32decode(secret.upper() + padding)

        hmac_digest = hmac.new(secret_bytes, counter_bytes, hashlib.sha1).digest()
        offset = hmac_digest[-1] & 0x0F
        code_int = (
            ((hmac_digest[offset] & 0x7F) << 24) |
            ((hmac_digest[offset + 1] & 0xFF) << 16) |
            ((hmac_digest[offset + 2] & 0xFF) << 8) |
            (hmac_digest[offset + 3] & 0xFF)
        )
        otp = str(code_int % (10 ** cls.DIGITS)).zfill(cls.DIGITS)
        return otp

    @classmethod
    def verify_otp(cls, secret: str, input_otp: str, window: int = 1) -> bool:
        current_time = int(time.time())
        for delta in range(-window, window + 1):
            check_time = current_time + (delta * cls.TIME_STEP)
            if cls.generate_otp(secret, check_time) == input_otp.strip():
                return True
        return False

class BackupCodeManager:
    """Generates and verifies single-use cryptographic recovery codes."""
    CODE_COUNT = 8

    @classmethod
    def generate_backup_codes(cls) -> List[str]:
        codes = []
        for _ in range(cls.CODE_COUNT):
            token = os.urandom(5).hex().upper()
            formatted = f"{token[:5]}-{token[5:]}"
            codes.append(formatted)
        return codes

    @classmethod
    def verify_and_consume(cls, submitted_code: str, active_codes: List[str]) -> Tuple[bool, List[str]]:
        clean_code = submitted_code.strip().upper()
        if clean_code in active_codes:
            remaining = [c for c in active_codes if c != clean_code]
            return (True, remaining)
        return (False, active_codes)
