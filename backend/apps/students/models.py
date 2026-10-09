from django.db import models
from django.conf import settings
from apps.academics.models import Department, Course, Branch, Semester

class StudentProfile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        ALUMNI = 'ALUMNI', 'Alumni'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile', null=True, blank=True)
    registration_no = models.CharField(max_length=30, unique=True, db_index=True)
    roll_no = models.CharField(max_length=30, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='students')
    admission_year = models.IntegerField(default=2024)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    contact_phone = models.CharField(max_length=20, blank=True, default='')
    parent_phone = models.CharField(max_length=20, blank=True, default='')
    address = models.TextField(blank=True, default='')
    is_eligible_for_exam = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['registration_no']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.roll_no} - {self.full_name} ({self.registration_no})"
