"""
AnalyticsService — computes and aggregates institutional KPIs for ExamForge.
Generates daily snapshots, department breakdowns, and trend data for the
governance dashboard and executive reports.
"""
import logging
from datetime import date, timedelta
from typing import Optional
from django.db import connection
from django.utils import timezone
from django.db.models import Count, Q, Avg, Sum

from .models import AnalyticsSnapshot, DepartmentMetric, SystemHealthLog, UserActivityLog

logger = logging.getLogger("examforge.analytics")


class AnalyticsService:
    """
    Computes ExamForge operational KPIs from live database data.

    Primary use cases:
    - Dashboard summary statistics (counts, rates, trends)
    - Periodic snapshot recording for trend analysis
    - Department-level performance metrics
    - System health monitoring
    """

    # ── Snapshot management ──────────────────────────────────────

    def record_daily_snapshot(self, target_date: Optional[date] = None) -> AnalyticsSnapshot:
        """
        Compute and persist a daily analytics snapshot.
        Idempotent — updates existing snapshot if one already exists for the date.
        """
        target_date = target_date or date.today()
        metrics = self._compute_base_metrics()

        snapshot, created = AnalyticsSnapshot.objects.update_or_create(
            period="daily",
            date=target_date,
            defaults=metrics,
        )
        action = "Created" if created else "Updated"
        logger.info("%s daily snapshot for %s: %s", action, target_date, metrics)
        return snapshot

    def _compute_base_metrics(self) -> dict:
        """Query live database for current institutional metrics."""
        from django.apps import apps
        metrics = {}

        # Students
        try:
            Student = apps.get_model("students", "Student")
            metrics["total_students"] = Student.objects.filter(is_active=True).count()
        except LookupError:
            metrics["total_students"] = 0

        # Faculty
        try:
            Faculty = apps.get_model("faculty", "Faculty")
            metrics["total_faculty"] = Faculty.objects.filter(is_active=True).count()
        except LookupError:
            metrics["total_faculty"] = 0

        # Exam sessions
        try:
            ExamSession = apps.get_model("examinations", "ExamSession")
            metrics["total_exam_sessions"] = ExamSession.objects.count()
            metrics["active_exam_sessions"] = ExamSession.objects.filter(status="active").count()
        except LookupError:
            metrics["total_exam_sessions"] = 0
            metrics["active_exam_sessions"] = 0

        # Registrations
        try:
            Registration = apps.get_model("registrations", "Registration")
            reg_qs = Registration.objects.values("status").annotate(cnt=Count("id"))
            reg_map = {r["status"]: r["cnt"] for r in reg_qs}
            metrics["total_registrations"] = sum(reg_map.values())
            metrics["approved_registrations"] = reg_map.get("approved", 0)
            metrics["pending_registrations"] = reg_map.get("pending", 0)
            metrics["rejected_registrations"] = reg_map.get("rejected", 0)
        except LookupError:
            metrics.update({
                "total_registrations": 0, "approved_registrations": 0,
                "pending_registrations": 0, "rejected_registrations": 0,
            })

        # Seating
        try:
            SeatingAllocation = apps.get_model("seating", "SeatingAllocation")
            metrics["seats_allocated"] = SeatingAllocation.objects.filter(is_active=True).count()
        except LookupError:
            metrics["seats_allocated"] = 0

        # Invigilation
        try:
            InvigilationDuty = apps.get_model("invigilation", "InvigilationDuty")
            metrics["invigilation_duties"] = InvigilationDuty.objects.filter(is_confirmed=True).count()
        except LookupError:
            metrics["invigilation_duties"] = 0

        return metrics

    # ── Dashboard data ──────────────────────────────────────

    def get_dashboard_summary(self) -> dict:
        """
        Compile a comprehensive summary dict for the admin dashboard.
        Pulls from the latest snapshot + live counts for freshness.
        """
        latest = AnalyticsSnapshot.objects.filter(period="daily").first()
        live = self._compute_base_metrics()
        trend_7d = self._compute_7day_trend()

        return {
            "summary": {**live},
            "rates": {
                "registration_approval_rate": self._safe_rate(
                    live.get("approved_registrations", 0),
                    live.get("total_registrations", 0)
                ),
                "hall_utilization_rate": latest.hall_utilization_rate if latest else 0.0,
            },
            "trends": trend_7d,
            "last_snapshot": str(latest.date) if latest else None,
        }

    def _compute_7day_trend(self) -> dict:
        """Return per-day student and registration counts for the past 7 days."""
        end = date.today()
        start = end - timedelta(days=6)
        snapshots = AnalyticsSnapshot.objects.filter(
            period="daily", date__range=[start, end]
        ).order_by("date")

        trend = []
        date_map = {s.date: s for s in snapshots}
        for i in range(7):
            d = start + timedelta(days=i)
            s = date_map.get(d)
            trend.append({
                "date": str(d),
                "students": s.total_students if s else None,
                "registrations": s.total_registrations if s else None,
                "seats_allocated": s.seats_allocated if s else None,
            })
        return {"daily": trend}

    # ── Department metrics ──────────────────────────────────────

    def compute_department_metrics(self, snapshot: AnalyticsSnapshot) -> list[DepartmentMetric]:
        """Build per-department breakdowns for a given snapshot."""
        created_metrics = []
        try:
            from django.apps import apps
            Department = apps.get_model("academics", "Department")
            departments = Department.objects.filter(is_active=True)

            for dept in departments:
                m, _ = DepartmentMetric.objects.update_or_create(
                    snapshot=snapshot,
                    department_code=dept.code,
                    defaults={
                        "department_name": dept.name,
                        "student_count": self._dept_student_count(dept.code),
                        "faculty_count": self._dept_faculty_count(dept.code),
                    }
                )
                created_metrics.append(m)
        except Exception as exc:
            logger.warning("compute_department_metrics failed: %s", exc)
        return created_metrics

    def _dept_student_count(self, dept_code: str) -> int:
        try:
            from django.apps import apps
            Student = apps.get_model("students", "Student")
            return Student.objects.filter(department__code=dept_code, is_active=True).count()
        except Exception:
            return 0

    def _dept_faculty_count(self, dept_code: str) -> int:
        try:
            from django.apps import apps
            Faculty = apps.get_model("faculty", "Faculty")
            return Faculty.objects.filter(department__code=dept_code, is_active=True).count()
        except Exception:
            return 0

    # ── System health ──────────────────────────────────────

    def record_health_check(self) -> SystemHealthLog:
        """Probe database response time and create a health log entry."""
        import time
        start = time.time()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_ms = int((time.time() - start) * 1000)
            status = "healthy" if db_ms < 100 else ("degraded" if db_ms < 500 else "critical")
        except Exception as exc:
            db_ms = None
            status = "critical"
            logger.error("Health check DB probe failed: %s", exc)

        try:
            from notifications.models import NotificationQueue
            pending = NotificationQueue.objects.filter(status="pending").count()
        except Exception:
            pending = 0

        return SystemHealthLog.objects.create(
            status=status,
            db_response_ms=db_ms,
            pending_notifications=pending,
        )

    def get_health_history(self, hours: int = 24) -> list:
        cutoff = timezone.now() - timedelta(hours=hours)
        return list(SystemHealthLog.objects.filter(
            timestamp__gte=cutoff
        ).values("timestamp", "status", "db_response_ms", "pending_notifications")
         .order_by("timestamp"))

    # ── User activity ──────────────────────────────────────

    def log_activity(self, user, action: str, resource_type: str = "",
                     resource_id: str = "", metadata: dict = None,
                     request=None) -> UserActivityLog:
        ip = None
        ua = ""
        if request:
            ip = self._get_client_ip(request)
            ua = request.META.get("HTTP_USER_AGENT", "")[:300]

        return UserActivityLog.objects.create(
            user=user,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            ip_address=ip,
            user_agent=ua,
            metadata=metadata or {},
        )

    def get_activity_summary(self, user, days: int = 30) -> dict:
        cutoff = timezone.now() - timedelta(days=days)
        logs = UserActivityLog.objects.filter(user=user, timestamp__gte=cutoff)
        by_action = dict(logs.values_list("action").annotate(cnt=Count("id")))
        return {
            "user": str(user),
            "period_days": days,
            "total_actions": logs.count(),
            "by_action": by_action,
        }

    # ── Utility ──────────────────────────────────────

    @staticmethod
    def _safe_rate(numerator: int, denominator: int) -> float:
        if denominator == 0:
            return 0.0
        return round(numerator / denominator * 100, 2)

    @staticmethod
    def _get_client_ip(request) -> Optional[str]:
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


analytics_service = AnalyticsService()
