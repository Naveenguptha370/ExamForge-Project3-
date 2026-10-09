from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.academics.models import Department

class Designation(models.TextChoices):
    PROFESSOR = 'PROFESSOR', _('Professor')
    ASSOC_PROF = 'ASSOC_PROF', _('Associate Professor')
    ASST_PROF = 'ASST_PROF', _('Assistant Professor')
    LECTURER = 'LECTURER', _('Lecturer / Adjunct')
    RESEARCH_FELLOW = 'RESEARCH_FELLOW', _('Research Fellow / Teaching Assistant')


class FacultyStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    ON_LEAVE = 'ON_LEAVE', _('On Leave')
    SABBATICAL = 'SABBATICAL', _('Sabbatical')
    RETIRED = 'RETIRED', _('Retired')


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='faculty_profile')
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    designation = models.CharField(max_length=30, choices=Designation.choices, default=Designation.ASST_PROF)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    status = models.CharField(max_length=20, choices=FacultyStatus.choices, default=FacultyStatus.ACTIVE)
    max_duties_per_session = models.PositiveIntegerField(default=10)
    current_duties_count = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True, default='')
    is_eligible_for_invigilation = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department__name', 'first_name']
        verbose_name = _('Faculty Profile')
        verbose_name_plural = _('Faculty Profiles')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_designation_display()}, {self.department.code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class ShiftSlot(models.TextChoices):
    MORNING = 'MORNING', _('Morning Shift')
    AFTERNOON = 'AFTERNOON', _('Afternoon Shift')
    EVENING = 'EVENING', _('Evening Shift')
    FULL_DAY = 'FULL_DAY', _('Full Day')


class FacultyAvailability(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(db_index=True)
    slot_shift = models.CharField(max_length=20, choices=ShiftSlot.choices, default=ShiftSlot.FULL_DAY)
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        unique_together = ('faculty', 'date', 'slot_shift')
        ordering = ['date', 'faculty__first_name']
        verbose_name = _('Faculty Availability')
        verbose_name_plural = _('Faculty Availabilities')

    def __str__(self):
        status = "Available" if self.is_available else f"Unavailable ({self.reason})"
        return f"{self.faculty.full_name} on {self.date} [{self.slot_shift}]: {status}"


class FacultyLeave(models.Model):
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='leaves')
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50, default='Medical / Personal')
    reason = models.TextField(blank=True, default='')
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('Faculty Leave')
        verbose_name_plural = _('Faculty Leaves')

    def __str__(self):
        return f"{self.faculty.full_name}: {self.start_date} to {self.end_date} ({self.leave_type})"
