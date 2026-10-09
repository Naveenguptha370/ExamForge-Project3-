from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.examinations.models import ExamSession, TimeSlot, ExamSubjectConfig
from apps.academics.models import Subject

class TimetableStatus(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft Generated')
    VALIDATING = 'VALIDATING', _('Validating Conflicts')
    VALIDATED = 'VALIDATED', _('Validated & Conflict-Free')
    APPROVED = 'APPROVED', _('Approved by Controller of Exams')
    PUBLISHED = 'PUBLISHED', _('Published')
    ARCHIVED = 'ARCHIVED', _('Archived')


class ClashType(models.TextChoices):
    STUDENT_OVERLAP = 'STUDENT_OVERLAP', _('Student Double-Booking')
    BRANCH_SEM_OVERLAP = 'BRANCH_SEM_OVERLAP', _('Branch & Semester Overlap')
    ROOM_CAPACITY_DEFICIT = 'ROOM_CAPACITY_DEFICIT', _('Room Capacity Deficit')
    FACULTY_UNAVAILABLE = 'FACULTY_UNAVAILABLE', _('Invigilator Availability Shortage')
    STUDY_GAP_VIOLATION = 'STUDY_GAP_VIOLATION', _('Insufficient Study Gap (Soft Constraint)')
    CONSECUTIVE_DIFFICULT = 'CONSECUTIVE_DIFFICULT', _('Consecutive Difficult Exams (Soft Constraint)')


class ClashSeverity(models.TextChoices):
    CRITICAL = 'CRITICAL', _('Critical (Mandatory Hard Clash)')
    HIGH = 'HIGH', _('High (Capacity/Resource Risk)')
    MEDIUM = 'MEDIUM', _('Medium (Soft Constraint Violation)')
    LOW = 'LOW', _('Low (Sub-optimal Spacing)')


class Timetable(models.Model):
    session = models.OneToOneField(ExamSession, on_delete=models.CASCADE, related_name='timetable')
    version = models.CharField(max_length=20, default='1.0')
    status = models.CharField(max_length=20, choices=TimetableStatus.choices, default=TimetableStatus.DRAFT, db_index=True)
    is_conflict_free = models.BooleanField(default=False)
    clash_count = models.PositiveIntegerField(default=0)
    total_exams_scheduled = models.PositiveIntegerField(default=0)
    total_slots_used = models.PositiveIntegerField(default=0)
    solver_duration_ms = models.FloatField(default=0.0)
    solver_iterations = models.PositiveIntegerField(default=0)
    solver_outcome = models.CharField(max_length=50, default='NOT_RUN')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_timetables')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_timetables')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Timetable')
        verbose_name_plural = _('Timetables')

    def __str__(self):
        return f"Timetable v{self.version} for {self.session.code} [{self.get_status_display()}]"

    @property
    def is_published(self):
        return self.status == TimetableStatus.PUBLISHED


class TimetableEntry(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='entries')
    subject_config = models.ForeignKey(ExamSubjectConfig, on_delete=models.CASCADE, related_name='timetable_entries')
    exam_date = models.DateField(db_index=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name='scheduled_entries')
    is_manual_override = models.BooleanField(default=False)
    has_conflict = models.BooleanField(default=False)
    conflict_details = models.CharField(max_length=255, blank=True, default='')
    expected_students = models.PositiveIntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('timetable', 'subject_config')
        ordering = ['exam_date', 'time_slot__start_time', 'subject_config__subject__code']
        verbose_name = _('Timetable Entry')
        verbose_name_plural = _('Timetable Entries')

    def __str__(self):
        return f"{self.exam_date} | {self.time_slot.name} | {self.subject_config.subject.code} - {self.subject_config.subject.name}"

    @property
    def subject(self):
        return self.subject_config.subject


class SchedulingClash(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='clashes')
    clash_type = models.CharField(max_length=30, choices=ClashType.choices, default=ClashType.STUDENT_OVERLAP)
    severity = models.CharField(max_length=20, choices=ClashSeverity.choices, default=ClashSeverity.CRITICAL)
    subject_1 = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='clashes_as_primary')
    subject_2 = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='clashes_as_secondary')
    exam_date = models.DateField(null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    affected_students_count = models.PositiveIntegerField(default=0)
    affected_student_names = models.JSONField(default=list, blank=True)
    suggested_resolution = models.TextField(blank=True, default='')
    is_resolved = models.BooleanField(default=False)
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-severity', 'exam_date']
        verbose_name = _('Scheduling Clash')
        verbose_name_plural = _('Scheduling Clashes')

    def __str__(self):
        return f"[{self.severity}] {self.get_clash_type_display()}: {self.subject_1.code} vs {self.subject_2.code if self.subject_2 else 'N/A'}"


class TimetableRevision(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    change_summary = models.TextField()
    diff_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Timetable Revision')
        verbose_name_plural = _('Timetable Revisions')

    def __str__(self):
        return f"Rev {self.revision_number} by {self.author.username if self.author else 'System'} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
