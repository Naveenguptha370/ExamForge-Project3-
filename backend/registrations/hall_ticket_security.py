"""
ExamForge M2 — Hall Ticket Cryptographic Security & Anti-Impersonation Engine
================================================================================
Generates cryptographically signed QR/Barcode verification payloads for official
examination hall tickets to prevent fraudulent reproduction or tampering during exam gate check-in.
"""

import hmac
import hashlib
import json
import base64
from typing import Dict, Any, List

DEFAULT_SECRET = "examforge-m2-hallticket-hmac-key-2026"

class HallTicketSecurityEngine:
    @classmethod
    def generate_security_digest(
        cls,
        roll_number: str,
        student_name: str,
        exam_session_code: str,
        subject_codes: List[str],
        secret_key: str = DEFAULT_SECRET
    ) -> Dict[str, Any]:
        """
        Creates a signed verification payload for printing on student hall ticket.
        """
        sorted_subjects = sorted(subject_codes)
        raw_message = f"{roll_number}|{exam_session_code}|{','.join(sorted_subjects)}"
        signature = hmac.new(
            secret_key.encode("utf-8"),
            raw_message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        # Short verification code for invigilator manual checks (first 8 chars of digest)
        short_verification_token = signature[:8].upper()

        payload = {
            "roll_no": roll_number,
            "name": student_name,
            "session": exam_session_code,
            "subject_count": len(sorted_subjects),
            "subjects": sorted_subjects,
            "verification_code": short_verification_token,
            "signature": signature
        }

        # Encode for QR scanner
        encoded_qr_string = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
        payload["qr_scanner_payload"] = encoded_qr_string
        return payload

    @classmethod
    def verify_ticket(
        cls,
        roll_number: str,
        exam_session_code: str,
        subject_codes: List[str],
        signature: str,
        secret_key: str = DEFAULT_SECRET
    ) -> bool:
        """
        Verifies that hall ticket details match the cryptographic signature.
        """
        sorted_subjects = sorted(subject_codes)
        raw_message = f"{roll_number}|{exam_session_code}|{','.join(sorted_subjects)}"
        expected_signature = hmac.new(
            secret_key.encode("utf-8"),
            raw_message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected_signature, signature)
