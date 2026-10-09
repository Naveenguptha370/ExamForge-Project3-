from django.db import models
from django.conf import settings
from apps.academics.models import Department

class FacultyProfile(models.Model):
    class Designation(models.TextChoices):
        PROFESSOR = 'PROFESSOR', 'Professor'
        ASSOC_PROFESSOR = 'ASSOC_PROFESSOR', 'Associate Professor'
        ASST_PROFESSOR = 'ASST_PROFESSOR', 'Assistant Professor'
        LECTURER = 'LECTURER', 'Lecturer'
        LAB_INSTRUCTOR = 'LAB_INSTRUCTOR', 'Lab Instructor'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=30, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    designation = models.CharField(max_length=30, choices=Designation.choices, default=Designation.ASST_PROFESSOR)
    qualification = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    emergency_contact = models.CharField(max_length=20, blank=True, default='')
    max_duties_per_term = models.IntegerField(default=6)
    is_available_for_duty = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username} ({self.get_designation_display()})"


class FacultyAvailability(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    time_slot_name = models.CharField(max_length=50, default='Morning', help_text='Morning, Afternoon or specific slot')
    is_available = models.BooleanField(default=True)
    reason = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ('faculty', 'date', 'time_slot_name')
        verbose_name_plural = 'Faculty Availabilities'

    def __str__(self):
        status = 'Available' if self.is_available else 'Unavailable'
        return f"{self.faculty.employee_id} on {self.date} ({self.time_slot_name}): {status}"


class FacultyLeave(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leave for {self.faculty.employee_id} ({self.start_date} to {self.end_date}) - {self.status}"
