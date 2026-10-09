from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = 'CREATE', 'Record Created'
        UPDATE = 'UPDATE', 'Record Updated'
        DELETE = 'DELETE', 'Record Deleted'
        APPROVE = 'APPROVE', 'Record Approved'
        PUBLISH = 'PUBLISH', 'Record Published'
        GENERATE = 'GENERATE', 'Generated (Solver/Seats/PDF)'
        BLOCK = 'BLOCK', 'Administrative Block'
        EXPORT = 'EXPORT', 'Data Exported'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=Action.choices)
    resource_type = models.CharField(max_length=60)
    resource_id = models.CharField(max_length=60, blank=True, default='')
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        actor = self.user.username if self.user else 'System'
        return f"{self.action} on {self.resource_type} by {actor} at {self.timestamp}"
