from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.academics.models import Department, Subject

class SessionType(models.TextChoices):
    END_TERM = 'END_TERM', _('End Semester Final Examination')
    MID_TERM = 'MID_TERM', _('Mid-Term / Continuous Assessment')
    SUPPLEMENTARY = 'SUPPLEMENTARY', _('Supplementary / Arrear Examination')
    SPECIAL_IMPROVEMENT = 'SPECIAL_IMPROVEMENT', _('Special Improvement Examination')


class SessionStatus(models.TextChoices):
    DRAFT = 'DRAFT', _('Draft (Configuring)')
    VALIDATING = 'VALIDATING', _('Validating Constraints')
    VALIDATED = 'VALIDATED', _('Validated & Conflict-Free')
    APPROVED = 'APPROVED', _('Approved by Controller of Exams')
    PUBLISHED = 'PUBLISHED', _('Published to Campus & Students')
    IN_PROGRESS = 'IN_PROGRESS', _('Examination In Progress')
    COMPLETED = 'COMPLETED', _('Completed & Evaluated')
    ARCHIVED = 'ARCHIVED', _('Archived (Historical Record)')


class ExamSession(models.Model):
    name = models.CharField(max_length=200, help_text="e.g. End Semester Examinations - Autumn 2025")
    code = models.CharField(max_length=50, unique=True, db_index=True, help_text="e.g. ESE-AUT-2025")
    academic_year = models.CharField(max_length=20, default='2025-2026')
    term = models.CharField(max_length=10, choices=[('ODD', 'Odd Term'), ('EVEN', 'Even Term'), ('SUMMER', 'Summer Term')], default='ODD')
    session_type = models.CharField(max_length=30, choices=SessionType.choices, default=SessionType.END_TERM)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    status = models.CharField(max_length=30, choices=SessionStatus.choices, default=SessionStatus.DRAFT, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_exam_sessions')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_exam_sessions')
    published_at = models.DateTimeField(null=True, blank=True)
    departments = models.ManyToManyField(Department, related_name='exam_sessions', blank=True)
    description = models.TextField(blank=True, default='')
    instructions = models.TextField(blank=True, default='Students must carry their physical Hall Ticket and College ID. Electronic devices strictly prohibited.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'code']
        verbose_name = _('Examination Session')
        verbose_name_plural = _('Examination Sessions')

    def __str__(self):
        return f"{self.name} [{self.code}] ({self.get_status_display()})"

    @property
    def is_published(self):
        return self.status in [SessionStatus.PUBLISHED, SessionStatus.IN_PROGRESS, SessionStatus.COMPLETED]

    @property
    def is_locked(self):
        return self.status in [SessionStatus.APPROVED, SessionStatus.PUBLISHED, SessionStatus.COMPLETED, SessionStatus.ARCHIVED]


class ShiftType(models.TextChoices):
    MORNING = 'MORNING', _('Morning Shift')
    AFTERNOON = 'AFTERNOON', _('Afternoon Shift')
    EVENING = 'EVENING', _('Evening Shift')


class TimeSlot(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Shift 1 (09:30 AM - 12:30 PM)")
    code = models.CharField(max_length=30, unique=True, db_index=True, help_text="e.g. M1, A1, E1")
    shift = models.CharField(max_length=20, choices=ShiftType.choices, default=ShiftType.MORNING)
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(default=180, help_text="Duration in minutes (e.g. 180 min = 3 hrs)")
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['sort_order', 'start_time']
        verbose_name = _('Time Slot')
        verbose_name_plural = _('Time Slots')

    def __str__(self):
        return f"{self.name} [{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}]"


class ExamSubjectConfig(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='configured_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_configs')
    expected_students_count = models.PositiveIntegerField(default=60)
    max_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=40)
    question_paper_code = models.CharField(max_length=50, blank=True, default='')
    difficulty_weight = models.PositiveIntegerField(default=3, help_text="Scale 1 (easiest) to 5 (most intense)")
    is_mandatory = models.BooleanField(default=True)
    is_practical = models.BooleanField(default=False)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_exam_configs')
    preferred_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL, null=True, blank=True, related_name='preferred_subjects')
    notes = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        unique_together = ('session', 'subject')
        ordering = ['subject__semester_number', 'subject__code']
        verbose_name = _('Exam Subject Configuration')
        verbose_name_plural = _('Exam Subject Configurations')

    def __str__(self):
        return f"{self.session.code} -> {self.subject.code}: {self.subject.name}"


class SchedulingConstraintConfig(models.Model):
    session = models.OneToOneField(ExamSession, on_delete=models.CASCADE, related_name='constraint_config')
    max_exams_per_student_per_day = models.PositiveIntegerField(default=1)
    min_study_gap_days_hard = models.PositiveIntegerField(default=1, help_text="Minimum rest days for heavy difficulty subjects")
    min_study_gap_days_general = models.PositiveIntegerField(default=0)
    prevent_cross_branch_clashes = models.BooleanField(default=True)
    allow_saturday_exams = models.BooleanField(default=True)
    allow_sunday_exams = models.BooleanField(default=False)
    max_concurrent_rooms = models.PositiveIntegerField(default=25)
    enforce_room_capacity_limits = models.BooleanField(default=True)
    enforce_invigilator_limits = models.BooleanField(default=True)
    consecutive_hard_subjects_penalty = models.PositiveIntegerField(default=50)
    solver_timeout_seconds = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Scheduling Constraint Configuration')
        verbose_name_plural = _('Scheduling Constraint Configurations')

    def __str__(self):
        return f"Constraints for {self.session.code}"


class ExamSessionHistory(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='history_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    state_from = models.CharField(max_length=50, blank=True, default='')
    state_to = models.CharField(max_length=50, blank=True, default='')
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('Exam Session History')
        verbose_name_plural = _('Exam Session History Logs')

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.session.code}: {self.action}"
