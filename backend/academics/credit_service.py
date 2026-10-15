"""
ExamForge M2 — CBCS Credit Accumulation & Academic Promotion Evaluator
========================================================================
Implements AICTE / UGC Choice Based Credit System (CBCS) rules for student
academic promotion between academic years and validates course prerequisite chains.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional

@dataclass
class PromotionEvaluation:
    is_promoted: bool
    status: str  # PROMOTED, ELIGIBLE_WITH_BACKLOGS, NOT_PROMOTED_CREDIT_SHORTAGE
    earned_credits: float
    required_credits: float
    credit_deficit: float
    remarks: str

class CBCSCreditEvaluator:
    # Minimum credit percentage required for promotion to next year
    PROMOTION_PERCENTAGE_RULES = {
        1: 50.0,  # Promotion to 2nd year: requires 50% of 1st year credits
        2: 60.0,  # Promotion to 3rd year: requires 60% of 1st & 2nd year credits
        3: 60.0,  # Promotion to 4th year: requires 60% of 1st, 2nd & 3rd year credits
    }

    @classmethod
    def evaluate_promotion(
        cls,
        from_year: int,
        total_registered_credits: float,
        earned_credits: float
    ) -> Dict[str, Any]:
        """
        Evaluates whether a student has earned enough credits to be promoted to next academic year.
        """
        required_pct = cls.PROMOTION_PERCENTAGE_RULES.get(from_year, 50.0)
        min_required_credits = (required_pct / 100.0) * total_registered_credits

        is_promoted = (earned_credits >= min_required_credits)
        deficit = max(0.0, min_required_credits - earned_credits)

        if is_promoted:
            has_backlogs = (earned_credits < total_registered_credits)
            status = "PROMOTED_WITH_BACKLOGS" if has_backlogs else "PROMOTED_CLEAR"
            remarks = f"Promoted to Year {from_year + 1}. Earned {earned_credits}/{total_registered_credits} credits."
        else:
            status = "DETAINED_CREDIT_SHORTAGE"
            remarks = f"Credit shortage. Required {min_required_credits} credits ({required_pct}%), but earned {earned_credits}. Deficit: {deficit} credits."

        return {
            "is_promoted": is_promoted,
            "status": status,
            "from_year": from_year,
            "target_year": from_year + 1 if is_promoted else from_year,
            "earned_credits": earned_credits,
            "min_required_credits": round(min_required_credits, 1),
            "deficit_credits": round(deficit, 1),
            "remarks": remarks
        }

    @classmethod
    def validate_prerequisites(
        cls,
        target_subject_code: str,
        completed_subject_codes: List[str],
        prerequisite_map: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Checks if student has cleared all mandatory prerequisite subjects.
        """
        required_prereqs = prerequisite_map.get(target_subject_code, [])
        missing = [p for p in required_prereqs if p not in completed_subject_codes]

        return {
            "target_subject": target_subject_code,
            "is_eligible": len(missing) == 0,
            "required_prerequisites": required_prereqs,
            "missing_prerequisites": missing,
            "remarks": "Prerequisites satisfied." if len(missing) == 0 else f"Missing required prerequisites: {', '.join(missing)}"
        }
