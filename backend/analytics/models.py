"""
Analytics models for ExamForge.
Stores aggregated institutional metrics, performance snapshots,
and operational KPI data for the governance dashboard.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class AnalyticsSnapshot(models.Model):
    """Point-in-time snapshot of institutional KPIs."""
    PERIOD_CHOICES = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("semester", "Semester"),
    ]
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    date = models.DateField()
    total_students = models.PositiveIntegerField(default=0)
    total_faculty = models.PositiveIntegerField(default=0)
    total_registrations = models.PositiveIntegerField(default=0)
    approved_registrations = models.PositiveIntegerField(default=0)
    pending_registrations = models.PositiveIntegerField(default=0)
    rejected_registrations = models.PositiveIntegerField(default=0)
    total_exam_sessions = models.PositiveIntegerField(default=0)
    active_exam_sessions = models.PositiveIntegerField(default=0)
    halls_utilized = models.PositiveIntegerField(default=0)
    total_hall_capacity = models.PositiveIntegerField(default=0)
    seats_allocated = models.PositiveIntegerField(default=0)
    invigilation_duties = models.PositiveIntegerField(default=0)
    hall_tickets_generated = models.PositiveIntegerField(default=0)
    attendance_recorded = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Analytics Snapshot"
        verbose_name_plural = "Analytics Snapshots"
        unique_together = [("period", "date")]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_period_display()} snapshot {self.date}"

    @property
    def registration_approval_rate(self) -> float:
        if self.total_registrations == 0:
            return 0.0
        return round(self.approved_registrations / self.total_registrations * 100, 2)

    @property
    def hall_utilization_rate(self) -> float:
        if self.total_hall_capacity == 0:
            return 0.0
        return round(self.seats_allocated / self.total_hall_capacity * 100, 2)


class DepartmentMetric(models.Model):
    """Per-department performance metrics for a specific exam session."""
    snapshot = models.ForeignKey(AnalyticsSnapshot, on_delete=models.CASCADE, related_name="department_metrics")
    department_code = models.CharField(max_length=10)
    department_name = models.CharField(max_length=100)
    student_count = models.PositiveIntegerField(default=0)
    registered_count = models.PositiveIntegerField(default=0)
    seated_count = models.PositiveIntegerField(default=0)
    absent_count = models.PositiveIntegerField(default=0)
    faculty_count = models.PositiveIntegerField(default=0)
    invigilation_duties_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Department Metric"
        verbose_name_plural = "Department Metrics"
        ordering = ["department_name"]

    def __str__(self):
        return f"{self.department_code} - {self.snapshot.date}"

    @property
    def registration_rate(self) -> float:
        if self.student_count == 0:
            return 0.0
        return round(self.registered_count / self.student_count * 100, 2)


class SystemHealthLog(models.Model):
    """Periodic health check records for system reliability monitoring."""
    STATUS_CHOICES = [
        ("healthy", "Healthy"),
        ("degraded", "Degraded"),
        ("critical", "Critical"),
    ]
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    db_response_ms = models.PositiveIntegerField(null=True, blank=True)
    api_response_ms = models.PositiveIntegerField(null=True, blank=True)
    active_sessions = models.PositiveIntegerField(default=0)
    pending_notifications = models.PositiveIntegerField(default=0)
    unprocessed_queue = models.PositiveIntegerField(default=0)
    disk_usage_pct = models.FloatField(null=True, blank=True)
    memory_usage_pct = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "System Health Log"
        verbose_name_plural = "System Health Logs"
        ordering = ["-timestamp"]
        get_latest_by = "timestamp"

    def __str__(self):
        return f"[{self.get_status_display()}] {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class UserActivityLog(models.Model):
    """Lightweight event log for user activity analytics (non-sensitive)."""
    ACTION_CHOICES = [
        ("login", "Login"),
        ("logout", "Logout"),
        ("view", "Page View"),
        ("create", "Resource Created"),
        ("update", "Resource Updated"),
        ("delete", "Resource Deleted"),
        ("export", "Data Exported"),
        ("report", "Report Generated"),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="activity_logs")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=60, blank=True)
    resource_id = models.CharField(max_length=60, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        verbose_name = "User Activity Log"
        verbose_name_plural = "User Activity Logs"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["user", "action"]),
            models.Index(fields=["resource_type", "timestamp"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
