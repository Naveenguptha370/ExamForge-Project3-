"""
ExamForge M2 — Student Examination Eligibility Evaluator
==========================================================
Enforces University / Autonomous College regulations for end-semester exam eligibility:
1. Standard minimum attendance requirement (75%).
2. Condonation range (65% to 74.9%) with medical certificate and condonation fee.
3. Detained status (< 65% attendance).
4. No-dues clearance and malpractice hold verification.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class EligibilityResult:
    is_eligible: bool
    status: str  # ELIGIBLE, CONDONATION_REQUIRED, DETAINED, ON_HOLD
    attendance_percentage: float
    condonation_fee: float
    reasons: list
    remarks: str

class StudentEligibilityEvaluator:
    STANDARD_ATTENDANCE_THRESHOLD = 75.0
    CONDONATION_MIN_THRESHOLD = 65.0
    BASE_CONDONATION_FEE = 1500.0  # Statutory condonation fee per regulation

    @classmethod
    def evaluate(
        cls,
        attendance_percentage: float,
        has_fee_dues: bool = False,
        has_disciplinary_hold: bool = False,
        has_medical_certificate: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates complete eligibility for generating exam hall ticket.
        """
        reasons = []
        condonation_fee = 0.0

        if has_disciplinary_hold:
            return {
                "is_eligible": False,
                "status": "DISCIPLINARY_HOLD",
                "attendance_percentage": round(attendance_percentage, 2),
                "condonation_fee": 0.0,
                "reasons": ["Student has an active disciplinary or malpractice inquiry hold."],
                "hall_ticket_allowed": False
            }

        if has_fee_dues:
            reasons.append("Tuition / Examination fee clearance pending.")

        if attendance_percentage >= cls.STANDARD_ATTENDANCE_THRESHOLD:
            if has_fee_dues:
                status = "FEE_HOLD"
                is_eligible = False
            else:
                status = "ELIGIBLE"
                is_eligible = True
        elif attendance_percentage >= cls.CONDONATION_MIN_THRESHOLD:
            if has_medical_certificate:
                condonation_fee = cls.BASE_CONDONATION_FEE
                if has_fee_dues:
                    status = "CONDONATION_FEE_AND_DUES_PENDING"
                    is_eligible = False
                else:
                    status = "CONDONATION_ELIGIBLE"
                    is_eligible = True
                reasons.append(f"Attendance in condonation bracket ({attendance_percentage}%). Medical condonation fee of Rs. {cls.BASE_CONDONATION_FEE} applicable.")
            else:
                status = "CONDONATION_DOCUMENT_REQUIRED"
                is_eligible = False
                reasons.append("Medical certificate required to process condonation for attendance between 65% and 75%.")
        else:
            status = "DETAINED"
            is_eligible = False
            reasons.append(f"Attendance below statutory minimum 65% ({attendance_percentage}%). Student is detained from current semester exams.")

        return {
            "is_eligible": is_eligible,
            "status": status,
            "attendance_percentage": round(attendance_percentage, 2),
            "condonation_fee": condonation_fee,
            "reasons": reasons,
            "hall_ticket_allowed": is_eligible and not has_fee_dues
        }
