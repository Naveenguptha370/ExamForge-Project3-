"""
ExamForge M2 — Registrations Models
=====================================
Handles subject registrations and exam registrations.
Depends on: accounts.User (M1), academics (M2), examinations (M3 stub).
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
import uuid


class RegistrationStatusChoices(models.TextChoices):
    PENDING    = 'pending',    'Pending'
    REGISTERED = 'registered', 'Registered'
    CONFIRMED  = 'confirmed',  'Confirmed'
    CANCELLED  = 'cancelled',  'Cancelled'
    WITHDRAWN  = 'withdrawn',  'Withdrawn'


class SubjectRegistration(models.Model):
    """
    Records a student's enrollment in a subject for a given academic semester.
    One student can register for the same subject only once per academic year.
    """
    id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student           = models.ForeignKey(
        'students.Student',
        on_delete=models.PROTECT,
        related_name='subject_registrations',
    )
    subject           = models.ForeignKey(
        'academics.Subject',
        on_delete=models.PROTECT,
        related_name='subject_registrations',
    )
    semester          = models.ForeignKey(
        'academics.Semester',
        on_delete=models.PROTECT,
        related_name='subject_registrations',
        null=True, blank=True,
    )
    academic_year     = models.ForeignKey(
        'academics.AcademicYear',
        on_delete=models.PROTECT,
        related_name='subject_registrations',
    )

    status            = models.CharField(
        max_length=20,
        choices=RegistrationStatusChoices.choices,
        default=RegistrationStatusChoices.REGISTERED,
        db_index=True,
    )
    registration_date = models.DateField(default=timezone.localdate)
    registered_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='subject_registrations_created',
    )
    cancelled_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='subject_registrations_cancelled',
    )
    cancelled_at      = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    remarks           = models.TextField(blank=True)

    # Bulk import tracking
    import_batch_id   = models.UUIDField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'm2_subject_registrations'
        verbose_name = 'Subject Registration'
        verbose_name_plural = 'Subject Registrations'
        ordering = ['-registration_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'academic_year'],
                condition=models.Q(status__in=['registered', 'confirmed']),
                name='unique_active_subject_registration',
            )
        ]
        indexes = [
            models.Index(fields=['student', 'academic_year']),
            models.Index(fields=['subject', 'academic_year']),
            models.Index(fields=['status', 'academic_year']),
        ]

    def __str__(self):
        return f"{self.student.roll_number} → {self.subject.code} ({self.academic_year})"

    def clean(self):
        super().clean()
        if self.student and not self.student.is_eligible_for_exam:
            raise ValidationError({
                'student': f"Student {self.student.roll_number} is not eligible for registration."
            })
        if self.student and self.subject:
            if hasattr(self.student, 'department') and hasattr(self.subject, 'department'):
                if self.student.department_id != self.subject.department_id:
                    raise ValidationError({
                        'subject': "Subject does not belong to the student's department."
                    })

    def cancel(self, cancelled_by=None, reason=''):
        self.status = RegistrationStatusChoices.CANCELLED
        self.cancelled_by = cancelled_by
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save(update_fields=['status', 'cancelled_by', 'cancelled_at', 'cancellation_reason', 'updated_at'])

    @property
    def is_active(self):
        return self.status in (RegistrationStatusChoices.REGISTERED, RegistrationStatusChoices.CONFIRMED)

    @property
    def student_name(self):
        return self.student.full_name if self.student_id else ''

    @property
    def student_roll(self):
        return self.student.roll_number if self.student_id else ''

    @property
    def subject_code(self):
        return self.subject.code if self.subject_id else ''

    @property
    def subject_name(self):
        return self.subject.name if self.subject_id else ''

    @property
    def academic_year_label(self):
        return str(self.academic_year) if self.academic_year_id else ''

    @property
    def semester_number(self):
        return self.semester.semester_number if self.semester_id else None


class ExamRegistration(models.Model):
    """
    Records a student's registration for a specific examination session.
    Links to M3's ExamSession via a nullable FK stub.
    """
    id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student           = models.ForeignKey(
        'students.Student',
        on_delete=models.PROTECT,
        related_name='exam_registrations',
    )
    subject           = models.ForeignKey(
        'academics.Subject',
        on_delete=models.PROTECT,
        related_name='exam_registrations',
    )
    academic_year     = models.ForeignKey(
        'academics.AcademicYear',
        on_delete=models.PROTECT,
        related_name='exam_registrations',
    )
    # M3 stub — will be a real FK when M3 is integrated
    exam_session_id   = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    exam_session_name = models.CharField(max_length=200, blank=True)

    status            = models.CharField(
        max_length=20,
        choices=RegistrationStatusChoices.choices,
        default=RegistrationStatusChoices.REGISTERED,
        db_index=True,
    )
    registration_date = models.DateField(default=timezone.localdate)
    registered_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='exam_registrations_created',
    )
    cancelled_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='exam_registrations_cancelled',
    )
    cancelled_at      = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    hall_ticket_number  = models.CharField(max_length=50, blank=True, db_index=True)
    remarks             = models.TextField(blank=True)
    import_batch_id     = models.UUIDField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'm2_exam_registrations'
        verbose_name = 'Exam Registration'
        verbose_name_plural = 'Exam Registrations'
        ordering = ['-registration_date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'academic_year', 'exam_session_id'],
                condition=models.Q(status__in=['registered', 'confirmed']),
                name='unique_active_exam_registration',
            )
        ]
        indexes = [
            models.Index(fields=['student', 'academic_year']),
            models.Index(fields=['subject', 'exam_session_id']),
        ]

    def __str__(self):
        return f"ExamReg: {self.student.roll_number} | {self.subject.code}"

    def clean(self):
        super().clean()
        if self.student and not self.student.is_eligible_for_exam:
            raise ValidationError({
                'student': f"Student {self.student.roll_number} is not exam eligible."
            })

    def cancel(self, cancelled_by=None, reason=''):
        self.status = RegistrationStatusChoices.CANCELLED
        self.cancelled_by = cancelled_by
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save(update_fields=['status', 'cancelled_by', 'cancelled_at', 'cancellation_reason', 'updated_at'])

    @property
    def student_name(self):
        return self.student.full_name if self.student_id else ''

    @property
    def student_roll(self):
        return self.student.roll_number if self.student_id else ''


class BulkRegistrationJob(models.Model):
    """
    Tracks a bulk CSV registration operation.
    """
    class JobStatus(models.TextChoices):
        QUEUED     = 'queued',     'Queued'
        PROCESSING = 'processing', 'Processing'
        COMPLETED  = 'completed',  'Completed'
        PARTIAL    = 'partial',    'Partial Success'
        FAILED     = 'failed',     'Failed'

    class RegistrationType(models.TextChoices):
        SUBJECT = 'subject', 'Subject Registration'
        EXAM    = 'exam',    'Exam Registration'

    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_id        = models.UUIDField(default=uuid.uuid4, db_index=True)
    registration_type = models.CharField(max_length=10, choices=RegistrationType.choices)
    academic_year   = models.ForeignKey(
        'academics.AcademicYear', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='bulk_jobs',
    )
    file_name       = models.CharField(max_length=255)
    status          = models.CharField(max_length=20, choices=JobStatus.choices, default=JobStatus.QUEUED)
    total_rows      = models.PositiveIntegerField(default=0)
    successful_rows = models.PositiveIntegerField(default=0)
    failed_rows     = models.PositiveIntegerField(default=0)
    duplicate_rows  = models.PositiveIntegerField(default=0)
    error_details   = models.JSONField(default=list)
    created_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='bulk_registration_jobs',
    )
    started_at      = models.DateTimeField(null=True, blank=True)
    completed_at    = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'm2_bulk_registration_jobs'
        verbose_name = 'Bulk Registration Job'
        verbose_name_plural = 'Bulk Registration Jobs'
        ordering = ['-created_at']

    def __str__(self):
        return f"BulkJob[{self.registration_type}] {self.file_name} — {self.status}"

    @property
    def success_rate(self):
        if not self.total_rows:
            return 0
        return round((self.successful_rows / self.total_rows) * 100, 1)
