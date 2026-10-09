"""
ExamForge - Faculty Subsystem Models
Member 1: Faculty Management
"""
from django.db import models
from django.conf import settings

class FacultyProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='faculty_profile')
    faculty_id = models.CharField(max_length=50, unique=True, db_index=True)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('ON_LEAVE', 'On Leave')], default='ACTIVE')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    qualification = models.CharField(max_length=150, blank=True, default='')
    specialization = models.CharField(max_length=200, blank=True, default='')
    date_of_joining = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['faculty_id']

    def __str__(self):
        return f"{self.faculty_id} - {self.email}"

class FacultyAvailability(models.Model):
    faculty = models.ForeignKey(FacultyProfile, related_name='availabilities', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=20, choices=[
        ('MONDAY','Monday'),('TUESDAY','Tuesday'),('WEDNESDAY','Wednesday'),
        ('THURSDAY','Thursday'),('FRIDAY','Friday'),('SATURDAY','Saturday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['faculty', 'day_of_week', 'start_time']

class FacultyLeave(models.Model):
    faculty = models.ForeignKey(FacultyProfile, related_name='leave_requests', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('PENDING','Pending'),('APPROVED','Approved'),('REJECTED','Rejected')], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
