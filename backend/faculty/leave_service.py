"""
ExamForge - Faculty Leave Workflow & Approval Ledger
Member 1: Faculty Management
"""
from typing import Dict, Any, Tuple, Optional
from datetime import date
from faculty.models import FacultyLeave

class LeaveStatus:
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

class FacultyLeaveService:
    @classmethod
    def apply_leave(cls, faculty_id: int, start_date: date, end_date: date, reason: str) -> Tuple[bool, str, Optional[FacultyLeave]]:
        if start_date > end_date:
            return (False, "Leave start date cannot be later than end date.", None)
        leave = FacultyLeave.objects.create(
            faculty_id=faculty_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status=LeaveStatus.PENDING
        )
        return (True, "Leave application submitted successfully.", leave)
