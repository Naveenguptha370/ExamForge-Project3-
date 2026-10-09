"""
ExamForge - Faculty Leave Workflow & Approval Ledger
Member 1: Faculty Management
"""
from typing import Dict, Any, Tuple, Optional
from datetime import date
from django.db import transaction
from faculty.models import FacultyLeave, FacultyProfile
from accounts.models import AuditLog, User

class LeaveStatus:
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CANCELLED = 'CANCELLED'

class FacultyLeaveService:
    """
    Manages leave requests, date conflict checks, and multi-tier administrative approvals.
    Prevents assignment of on-leave faculty to examination duties.
    """

    @classmethod
    def apply_leave(
        cls,
        faculty_id: int,
        start_date: date,
        end_date: date,
        reason: str
    ) -> Tuple[bool, str, Optional[FacultyLeave]]:
        if start_date > end_date:
            return (False, "Leave start date cannot be later than end date.", None)
        if start_date < date.today():
            return (False, "Leave cannot be requested for historical dates.", None)

        # Check existing overlapping leaves
        existing = FacultyLeave.objects.filter(
            faculty_id=faculty_id,
            status__in=[LeaveStatus.PENDING, LeaveStatus.APPROVED],
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()

        if existing:
            return (False, "An overlapping leave request already exists for this period.", None)

        leave = FacultyLeave.objects.create(
            faculty_id=faculty_id,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status=LeaveStatus.PENDING
        )
        return (True, "Leave application submitted successfully.", leave)

    @classmethod
    @transaction.atomic
    def process_approval(
        cls,
        leave_id: int,
        actor: User,
        approve: bool,
        remarks: str = ""
    ) -> Tuple[bool, str]:
        try:
            leave = FacultyLeave.objects.select_for_update().get(id=leave_id)
        except FacultyLeave.DoesNotExist:
            return (False, "Leave record not found.")

        if leave.status != LeaveStatus.PENDING:
            return (False, f"Leave has already been processed with status: {leave.status}")

        new_status = LeaveStatus.APPROVED if approve else LeaveStatus.REJECTED
        leave.status = new_status
        leave.save(update_fields=['status'])

        # If approved and current date falls in leave window, update profile status
        today = date.today()
        if approve and leave.start_date <= today <= leave.end_date:
            profile = leave.faculty
            profile.status = 'ON_LEAVE'
            profile.save(update_fields=['status'])

        AuditLog.objects.create(
            actor=actor,
            action=f"FACULTY_LEAVE_{new_status}",
            model_name="FacultyLeave",
            object_id=str(leave.id),
            details=f"Leave {new_status.lower()} by {actor.username}. Remarks: {remarks}"
        )
        return (True, f"Leave request marked as {new_status}.")
