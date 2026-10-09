from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_records')
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100, blank=True, default='')
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')

    def __str__(self):
        user_str = self.user.username if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user_str}: {self.action} on {self.resource_type}"


class SystemSetting(models.Model):
    key = models.CharField(max_length=100, unique=True, db_index=True)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True, default='')
    is_public = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']
        verbose_name = _('System Setting')
        verbose_name_plural = _('System Settings')

    def __str__(self):
        return f"{self.key} = {self.value[:30]}"
