"""
Automated Unit Tests for CBCS Credit Accumulation and Prerequisite Validation Engine.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from academics.credit_service import CBCSCreditEvaluator

def test_promotion_clear():
    # Year 1 (40 credits total, earned 40) -> Promoted
    res = CBCSCreditEvaluator.evaluate_promotion(from_year=1, total_registered_credits=40.0, earned_credits=40.0)
    assert res["is_promoted"] is True
    assert res["status"] == "PROMOTED_CLEAR"
    assert res["target_year"] == 2

def test_promotion_with_backlogs():
    # Year 1 (40 credits total, earned 24 >= 50% min 20) -> Promoted with backlogs
    res = CBCSCreditEvaluator.evaluate_promotion(from_year=1, total_registered_credits=40.0, earned_credits=24.0)
    assert res["is_promoted"] is True
    assert res["status"] == "PROMOTED_WITH_BACKLOGS"
    assert res["deficit_credits"] == 0.0

def test_credit_detention():
    # Year 1 (40 credits total, earned 16 < 50% min 20) -> Detained
    res = CBCSCreditEvaluator.evaluate_promotion(from_year=1, total_registered_credits=40.0, earned_credits=16.0)
    assert res["is_promoted"] is False
    assert res["status"] == "DETAINED_CREDIT_SHORTAGE"
    assert res["deficit_credits"] == 4.0

def test_prerequisite_satisfied():
    prereq_map = {
        "CS401_DATA_STRUCTURES": ["CS301_PROGRAMMING_FUNDAMENTALS"],
        "CS501_ALGORITHMS": ["CS401_DATA_STRUCTURES"]
    }
    completed = ["CS301_PROGRAMMING_FUNDAMENTALS"]
    res = CBCSCreditEvaluator.validate_prerequisites("CS401_DATA_STRUCTURES", completed, prereq_map)
    assert res["is_eligible"] is True
    assert len(res["missing_prerequisites"]) == 0

def test_prerequisite_missing():
    prereq_map = {
        "CS501_ALGORITHMS": ["CS401_DATA_STRUCTURES", "CS302_DISCRETE_MATH"]
    }
    completed = ["CS401_DATA_STRUCTURES"]
    res = CBCSCreditEvaluator.validate_prerequisites("CS501_ALGORITHMS", completed, prereq_map)
    assert res["is_eligible"] is False
    assert "CS302_DISCRETE_MATH" in res["missing_prerequisites"]

if __name__ == "__main__":
    test_promotion_clear()
    test_promotion_with_backlogs()
    test_credit_detention()
    test_prerequisite_satisfied()
    test_prerequisite_missing()
    print("All CBCS credit evaluator and prerequisite tests passed successfully!")
