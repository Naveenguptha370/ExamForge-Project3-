from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class TargetRole(models.TextChoices):
    ALL = 'ALL', _('All Campus Users')
    FACULTY = 'FACULTY', _('Faculty & Invigilators')
    STUDENTS = 'STUDENTS', _('Students Only')
    STAFF = 'STAFF', _('Examination Staff')


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    target_role = models.CharField(max_length=20, choices=TargetRole.choices, default=TargetRole.ALL)
    is_pinned = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-created_at']
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')

    def __str__(self):
        return f"[{self.target_role}] {self.title}"


class SystemNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=150)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, default='INFO')  # INFO, WARNING, SUCCESS, URGENT
    is_read = models.BooleanField(default=False)
    link_url = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('System Notification')
        verbose_name_plural = _('System Notifications')

    def __str__(self):
        return f"{self.user.username}: {self.title}"
