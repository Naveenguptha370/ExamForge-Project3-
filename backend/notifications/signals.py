"""
Django signals for ExamForge notification triggers.
Connects domain events (exam published, seating assigned, duty allocated) to the
notification dispatch pipeline automatically.
"""
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.contrib.auth import get_user_model

from .service import notification_service

logger = logging.getLogger("examforge.notifications.signals")
User = get_user_model()

# ── Custom domain signals ──────────────────────────────────────

exam_timetable_published = Signal()
"""
Fired when an exam timetable is officially published.
providing_args: ["timetable_id", "session_name", "published_by_id", "student_ids"]
"""

seating_plan_generated = Signal()
"""
Fired when a seating plan is finalized for a session.
providing_args: ["session_id", "session_name", "hall_ids", "student_ids"]
"""

invigilation_duty_assigned = Signal()
"""
Fired when invigilator duties are allocated.
providing_args: ["session_id", "session_name", "faculty_id", "hall_name", "duty_date"]
"""

hall_ticket_generated = Signal()
"""
Fired when a hall ticket PDF is generated for a student.
providing_args: ["student_id", "student_name", "exam_session", "hall_ticket_url"]
"""

registration_approved = Signal()
"""
Fired when an exam registration is approved for a student.
providing_args: ["student_id", "student_name", "session_name", "course_names"]
"""

registration_rejected = Signal()
"""
Fired when an exam registration is rejected.
providing_args: ["student_id", "student_name", "session_name", "reason"]
"""

# ── Signal handlers ──────────────────────────────────────


@receiver(exam_timetable_published)
def on_timetable_published(sender, **kwargs):
    """Notify all registered students when timetable is published."""
    session_name = kwargs.get("session_name", "Upcoming Examination")
    student_ids = kwargs.get("student_ids", [])
    published_by = kwargs.get("published_by_id")

    if not student_ids:
        logger.warning("timetable_published signal: no student_ids provided")
        return

    notifications = notification_service.notify_users(
        user_ids=student_ids,
        template_code="exam.timetable.published",
        context={
            "session_name": session_name,
            "action": "View Timetable",
        },
        action_url="/timetable",
        action_label="View Timetable",
        priority=2,
    )
    logger.info(
        "Timetable published: %d notifications sent for session '%s'",
        len(notifications), session_name
    )


@receiver(seating_plan_generated)
def on_seating_plan_generated(sender, **kwargs):
    """Notify students of their assigned seat when seating plan is ready."""
    session_name = kwargs.get("session_name", "Upcoming Examination")
    student_ids = kwargs.get("student_ids", [])

    notifications = notification_service.notify_users(
        user_ids=student_ids,
        template_code="seating.plan.published",
        context={"session_name": session_name},
        action_url="/seating",
        action_label="View Seat",
        priority=2,
    )
    logger.info(
        "Seating plan: %d student notifications dispatched for session '%s'",
        len(notifications), session_name
    )


@receiver(invigilation_duty_assigned)
def on_invigilation_duty_assigned(sender, **kwargs):
    """Notify a faculty member of their invigilation duty assignment."""
    faculty_id = kwargs.get("faculty_id")
    session_name = kwargs.get("session_name", "Examination")
    hall_name = kwargs.get("hall_name", "")
    duty_date = kwargs.get("duty_date", "")

    if not faculty_id:
        return

    notification_service.notify_user(
        user_id=faculty_id,
        template_code="invigilation.duty.assigned",
        context={
            "session_name": session_name,
            "hall_name": hall_name,
            "duty_date": duty_date,
        },
        action_url="/invigilation/duties",
        action_label="View Duty Details",
        priority=2,
    )
    logger.info("Duty assigned notification sent to faculty %s", faculty_id)


@receiver(hall_ticket_generated)
def on_hall_ticket_generated(sender, **kwargs):
    """Notify student when their hall ticket is ready for download."""
    student_id = kwargs.get("student_id")
    student_name = kwargs.get("student_name", "Student")
    exam_session = kwargs.get("exam_session", "Examination")
    ticket_url = kwargs.get("hall_ticket_url", "/hall-tickets")

    if not student_id:
        return

    notification_service.notify_user(
        user_id=student_id,
        template_code="hall_ticket.generated",
        context={
            "student_name": student_name,
            "exam_session": exam_session,
        },
        action_url=ticket_url,
        action_label="Download Hall Ticket",
        priority=1,
        expires_hours=72,
    )
    logger.info("Hall ticket notification sent to student %s", student_id)


@receiver(registration_approved)
def on_registration_approved(sender, **kwargs):
    student_id = kwargs.get("student_id")
    session_name = kwargs.get("session_name", "Examination")
    course_names = ", ".join(kwargs.get("course_names", []))

    if not student_id:
        return

    notification_service.notify_user(
        user_id=student_id,
        template_code="registration.approved",
        context={
            "session_name": session_name,
            "course_names": course_names,
        },
        action_url="/registrations",
        action_label="View Registration",
        priority=2,
    )


@receiver(registration_rejected)
def on_registration_rejected(sender, **kwargs):
    student_id = kwargs.get("student_id")
    session_name = kwargs.get("session_name", "Examination")
    reason = kwargs.get("reason", "Please contact the examination office.")

    if not student_id:
        return

    notification_service.notify_user(
        user_id=student_id,
        template_code="registration.rejected",
        context={
            "session_name": session_name,
            "reason": reason,
        },
        action_url="/registrations",
        action_label="View Registration Status",
        priority=2,
    )
