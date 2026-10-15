"""
Automated Unit Tests for Student Exam Eligibility and Condonation Evaluator.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from students.eligibility_service import StudentEligibilityEvaluator

def test_standard_eligible():
    res = StudentEligibilityEvaluator.evaluate(attendance_percentage=82.5, has_fee_dues=False)
    assert res["is_eligible"] is True
    assert res["status"] == "ELIGIBLE"
    assert res["hall_ticket_allowed"] is True
    assert res["condonation_fee"] == 0.0

def test_condonation_with_medical_cert():
    res = StudentEligibilityEvaluator.evaluate(
        attendance_percentage=68.0,
        has_fee_dues=False,
        has_medical_certificate=True
    )
    assert res["is_eligible"] is True
    assert res["status"] == "CONDONATION_ELIGIBLE"
    assert res["condonation_fee"] == 1500.0

def test_condonation_missing_medical_cert():
    res = StudentEligibilityEvaluator.evaluate(
        attendance_percentage=70.0,
        has_fee_dues=False,
        has_medical_certificate=False
    )
    assert res["is_eligible"] is False
    assert res["status"] == "CONDONATION_DOCUMENT_REQUIRED"

def test_detained_student():
    res = StudentEligibilityEvaluator.evaluate(attendance_percentage=58.2)
    assert res["is_eligible"] is False
    assert res["status"] == "DETAINED"
    assert res["hall_ticket_allowed"] is False

def test_disciplinary_hold():
    res = StudentEligibilityEvaluator.evaluate(attendance_percentage=90.0, has_disciplinary_hold=True)
    assert res["is_eligible"] is False
    assert res["status"] == "DISCIPLINARY_HOLD"

if __name__ == "__main__":
    test_standard_eligible()
    test_condonation_with_medical_cert()
    test_condonation_missing_medical_cert()
    test_detained_student()
    test_disciplinary_hold()
    print("All student eligibility evaluator unit tests passed successfully!")
