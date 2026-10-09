from django.db import models
from django.conf import settings

class Announcement(models.Model):
    class TargetRole(models.TextChoices):
        ALL = 'ALL', 'Everyone'
        STUDENT = 'STUDENT', 'Students Only'
        FACULTY = 'FACULTY', 'Faculty Only'
        EXAM_STAFF = 'EXAM_STAFF', 'Examination Staff Only'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        NORMAL = 'NORMAL', 'Normal'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    title = models.CharField(max_length=200)
    content = models.TextField()
    target_role = models.CharField(max_length=20, choices=TargetRole.choices, default=TargetRole.ALL)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.NORMAL)
    is_active = models.BooleanField(default=True)
    published_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.priority}] {self.title} ({self.target_role})"


class InAppNotification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, default='GENERAL')
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.title} ({'Read' if self.is_read else 'Unread'})"
