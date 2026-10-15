"""
Notification system models for ExamForge.
Handles in-app, email, and SMS notification delivery with full audit trail.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Q
import uuid

User = get_user_model()


class NotificationCategory(models.Model):
    """Top-level grouping for notification types."""
    CATEGORY_CHOICES = [
        ("exam", "Examination"),
        ("seating", "Seating Assignment"),
        ("invigilation", "Invigilation Duty"),
        ("hall_ticket", "Hall Ticket"),
        ("attendance", "Attendance"),
        ("registration", "Registration"),
        ("system", "System"),
        ("academic", "Academic"),
    ]
    code = models.CharField(max_length=30, unique=True, choices=CATEGORY_CHOICES)
    label = models.CharField(max_length=80)
    icon = models.CharField(max_length=30, default="bell")
    color = models.CharField(max_length=20, default="#2D6A4F")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification Category"
        verbose_name_plural = "Notification Categories"
        ordering = ["label"]

    def __str__(self):
        return self.label


class NotificationTemplate(models.Model):
    """Reusable notification message templates with variable substitution."""
    CHANNEL_CHOICES = [
        ("in_app", "In-App"),
        ("email", "Email"),
        ("sms", "SMS"),
        ("push", "Push Notification"),
    ]
    code = models.CharField(max_length=60, unique=True)
    category = models.ForeignKey(NotificationCategory, on_delete=models.PROTECT)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="in_app")
    subject_template = models.CharField(max_length=200)
    body_template = models.TextField()
    available_variables = models.JSONField(default=list, help_text="List of variable names usable in template")
    is_active = models.BooleanField(default=True)
    requires_confirmation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notification Template"
        verbose_name_plural = "Notification Templates"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} ({self.get_channel_display()})"

    def render(self, context: dict) -> tuple[str, str]:
        """Render subject and body with provided context variables."""
        subject = self.subject_template
        body = self.body_template
        for key, value in context.items():
            subject = subject.replace(f"{{{{{key}}}}}", str(value))
            body = body.replace(f"{{{{{key}}}}}", str(value))
        return subject, body


class NotificationQueue(models.Model):
    """Pending notifications queued for delivery."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("sent", "Sent"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]
    PRIORITY_CHOICES = [
        (1, "Critical"),
        (2, "High"),
        (3, "Normal"),
        (4, "Low"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queued_notifications")
    template = models.ForeignKey(NotificationTemplate, on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(NotificationCategory, on_delete=models.SET_NULL, null=True)
    channel = models.CharField(max_length=20, default="in_app")
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    context_data = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    scheduled_at = models.DateTimeField(default=timezone.now)
    sent_at = models.DateTimeField(null=True, blank=True)
    failure_reason = models.TextField(blank=True)
    retry_count = models.PositiveSmallIntegerField(default=0)
    max_retries = models.PositiveSmallIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification Queue Entry"
        verbose_name_plural = "Notification Queue"
        ordering = ["priority", "scheduled_at"]
        indexes = [
            models.Index(fields=["status", "scheduled_at"]),
            models.Index(fields=["recipient", "status"]),
        ]

    def __str__(self):
        return f"{self.subject[:50]} -> {self.recipient}"

    def mark_sent(self):
        self.status = "sent"
        self.sent_at = timezone.now()
        self.save(update_fields=["status", "sent_at"])

    def mark_failed(self, reason: str):
        self.failure_reason = reason
        self.retry_count += 1
        if self.retry_count >= self.max_retries:
            self.status = "failed"
        else:
            self.status = "pending"
        self.save(update_fields=["status", "failure_reason", "retry_count"])


class Notification(models.Model):
    """Delivered in-app notification record visible to users."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    category = models.ForeignKey(NotificationCategory, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    action_url = models.CharField(max_length=300, blank=True)
    action_label = models.CharField(max_length=60, blank=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["recipient", "created_at"]),
        ]

    def __str__(self):
        return f"[{self.recipient}] {self.subject}"

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        return timezone.now() > self.expires_at


class NotificationPreference(models.Model):
    """Per-user, per-category notification channel preferences."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_preferences")
    category = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE)
    in_app_enabled = models.BooleanField(default=True)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"
        unique_together = [("user", "category")]

    def __str__(self):
        return f"{self.user} - {self.category}"


class NotificationBatch(models.Model):
    """Bulk notification jobs (e.g., broadcast to all students of a batch)."""
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("scheduled", "Scheduled"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.PROTECT)
    target_roles = models.JSONField(default=list)
    target_user_ids = models.JSONField(default=list)
    context_data = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    total_recipients = models.PositiveIntegerField(default=0)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_batches")
    created_at = models.DateTimeField(auto_now_add=True)
    error_log = models.TextField(blank=True)

    class Meta:
        verbose_name = "Notification Batch"
        verbose_name_plural = "Notification Batches"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def success_rate(self) -> float:
        if self.total_recipients == 0:
            return 0.0
        return round(self.sent_count / self.total_recipients * 100, 2)
