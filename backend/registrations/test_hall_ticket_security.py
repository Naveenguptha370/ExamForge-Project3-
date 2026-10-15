"""
Automated Unit Tests for Hall Ticket Security & Cryptographic Digest Engine.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from registrations.hall_ticket_security import HallTicketSecurityEngine

def test_generate_and_verify_hall_ticket():
    roll = "22B91A0501"
    name = "K. Nagaraju"
    session = "NOV-DEC-2026-REGULAR"
    subjects = ["CS501", "CS502", "CS503", "CS504"]

    payload = HallTicketSecurityEngine.generate_security_digest(roll, name, session, subjects)
    assert payload["roll_no"] == roll
    assert payload["verification_code"] is not None
    assert len(payload["verification_code"]) == 8
    assert payload["signature"] is not None

    # Verification success
    is_valid = HallTicketSecurityEngine.verify_ticket(roll, session, subjects, payload["signature"])
    assert is_valid is True

def test_tamper_detection():
    roll = "22B91A0501"
    name = "K. Nagaraju"
    session = "NOV-DEC-2026-REGULAR"
    subjects = ["CS501", "CS502"]

    payload = HallTicketSecurityEngine.generate_security_digest(roll, name, session, subjects)
    
    # Tampered subjects list (trying to sit for unauthorized exam CS599)
    tampered_subjects = ["CS501", "CS502", "CS599"]
    is_valid = HallTicketSecurityEngine.verify_ticket(roll, session, tampered_subjects, payload["signature"])
    assert is_valid is False

def test_invalid_roll_tamper():
    roll = "22B91A0501"
    session = "NOV-DEC-2026-REGULAR"
    subjects = ["CS501"]

    payload = HallTicketSecurityEngine.generate_security_digest(roll, "Student A", session, subjects)
    
    # Trying to reuse signature with another roll number
    is_valid = HallTicketSecurityEngine.verify_ticket("22B91A0599", session, subjects, payload["signature"])
    assert is_valid is False

if __name__ == "__main__":
    test_generate_and_verify_hall_ticket()
    test_tamper_detection()
    test_invalid_roll_tamper()
    print("All hall ticket security digest tests passed successfully!")
