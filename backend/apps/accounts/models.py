from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', _('Administrator')
    FACULTY = 'FACULTY', _('Faculty / Invigilator')
    EXAM_STAFF = 'EXAM_STAFF', _('Examination Staff')
    STUDENT = 'STUDENT', _('Student')

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        db_index=True
    )
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    department_name = models.CharField(max_length=100, blank=True, null=True)
    employee_or_roll_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=True)
    must_change_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'role']

    class Meta:
        ordering = ['-date_joined']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_faculty(self):
        return self.role == UserRole.FACULTY

    @property
    def is_exam_staff(self):
        return self.role == UserRole.EXAM_STAFF

    @property
    def is_student(self):
        return self.role == UserRole.STUDENT


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activities')
    action = models.CharField(max_length=255)
    module = models.CharField(max_length=100, default='SYSTEM')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('User Activity')
        verbose_name_plural = _('User Activities')

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {username} - {self.action}"
