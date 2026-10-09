from django.db import models
from django.conf import settings
from apps.academics.models import Subject

class ExamSession(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        VALIDATED = 'VALIDATED', 'Validated'
        APPROVED = 'APPROVED', 'Approved'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    class SessionType(models.TextChoices):
        REGULAR = 'REGULAR', 'Regular Semester Examination'
        SUPPLEMENTARY = 'SUPPLEMENTARY', 'Supplementary / Backlog Examination'
        MIDTERM = 'MIDTERM', 'Mid-Term Examination'
        SPECIAL = 'SPECIAL', 'Special Examination'

    name = models.CharField(max_length=150)
    session_code = models.CharField(max_length=50, unique=True)
    academic_year = models.CharField(max_length=20, default='2025-2026')
    term = models.CharField(max_length=10, default='EVEN')
    session_type = models.CharField(max_length=30, choices=SessionType.choices, default=SessionType.REGULAR)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    instructions = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.session_code} - {self.name} ({self.status})"


class TimeSlot(models.Model):
    name = models.CharField(max_length=100)
    slot_code = models.CharField(max_length=30, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"


class ExamSubject(models.Model):
    exam_session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='exam_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_instances')
    planned_date = models.DateField(null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='exam_subjects')
    duration_minutes = models.IntegerField(default=180)
    max_marks = models.IntegerField(default=100)
    is_scheduled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('exam_session', 'subject')
        ordering = ['planned_date', 'time_slot__start_time']

    def __str__(self):
        return f"{self.exam_session.session_code}: {self.subject.code}"
