from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrator'
        FACULTY = 'FACULTY', 'Faculty / Invigilator'
        EXAM_STAFF = 'EXAM_STAFF', 'Examination Staff'
        STUDENT = 'STUDENT', 'Student'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        PENDING = 'PENDING', 'Pending'
        ARCHIVED = 'ARCHIVED', 'Archived'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=20, blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_faculty(self):
        return self.role == self.Role.FACULTY

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.username} ({self.role})'

class AuditLog(models.Model):
    actor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_actions')
    action = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100, blank=True, default='')
    object_id = models.CharField(max_length=255, blank=True, default='')
    details = models.TextField(blank=True, default='')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} - {self.model_name}'
