"""
ExamForge M2 — Student Management Models
==========================================
Defines the Student model and related records.

Design Decisions:
- Student does NOT inherit from Django's AbstractUser.
  M1 owns the User model. Students get a linked User account
  optionally — the Student model holds academic profile data.
- All academic FK references point to M2's Academic models.
- Soft delete via 'status' field (active / inactive / graduated / suspended / withdrawn).
- Duplicate prevention enforced at DB level via unique constraints.

Integration Notes:
- M1: Student.user → ForeignKey(settings.AUTH_USER_MODEL)
  M1 creates/manages the user account; M2 manages the academic profile.
- M3: Examinations reference Student records for eligibility.
- M4: Seating module fetches students by department/course/branch/semester.
- M5: Hall tickets use this model for student name, roll number, photo, etc.
"""

import uuid
import logging
from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
    EmailValidator,
)
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

from academics.models import (
    Department,
    Course,
    Branch,
    Semester,
    AcademicYear,
    StatusChoices,
)

logger = logging.getLogger(__name__)


# ─── Constants ───────────────────────────────────────────────────────────────────

class StudentStatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    GRADUATED = 'graduated', 'Graduated'
    SUSPENDED = 'suspended', 'Suspended'
    WITHDRAWN = 'withdrawn', 'Withdrawn'
    DETAINED = 'detained', 'Detained'


class GenderChoices(models.TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'
    PREFER_NOT_TO_SAY = 'prefer_not_to_say', 'Prefer not to say'


class BloodGroupChoices(models.TextChoices):
    A_POS = 'A+', 'A+'
    A_NEG = 'A-', 'A-'
    B_POS = 'B+', 'B+'
    B_NEG = 'B-', 'B-'
    O_POS = 'O+', 'O+'
    O_NEG = 'O-', 'O-'
    AB_POS = 'AB+', 'AB+'
    AB_NEG = 'AB-', 'AB-'
    UNKNOWN = 'unknown', 'Unknown'


# ─── Validators ──────────────────────────────────────────────────────────────────
phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{6,14}$',
    message='Enter a valid phone number (7 to 15 digits, optionally starting with +).',
)

roll_number_validator = RegexValidator(
    regex=r'^[A-Z0-9\-\/]{3,20}$',
    message='Roll number must be 3-20 characters: uppercase letters, digits, hyphens, or slashes.',
)


# ─── Student Model ────────────────────────────────────────────────────────────────
class Student(models.Model):
    """
    Core student academic profile.

    Fields are divided into:
    - Identity: student_id, roll_number, full_name
    - Contact: email, phone
    - Academic: department, course, branch, current_semester, academic_year
    - Personal: gender, date_of_birth, blood_group (non-sensitive, institution-standard)
    - System: status, created_at, created_by, updated_at, updated_by

    Uniqueness:
    - roll_number: globally unique (or unique per academic year — see constraint).
    - institutional_email: unique.
    - user: unique OneToOne.
    """

    # ── Primary Key ──────────────────────────────────────────────────────────────
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text='Unique UUID for this student record.',
    )

    # ── Link to M1's User Model (Optional) ──────────────────────────────────────
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile',
        help_text='Linked user account (managed by M1).',
    )

    # ── Identity ─────────────────────────────────────────────────────────────────
    student_id = models.CharField(
        max_length=30,
        unique=True,
        help_text='Institutional student ID, auto-generated or assigned during enrollment.',
    )
    roll_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[roll_number_validator],
        db_index=True,
        help_text='Examination roll number, unique across the institution.',
    )
    full_name = models.CharField(
        max_length=200,
        help_text='Full legal name of the student.',
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='First name.',
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='Last name or surname.',
    )

    # ── Contact ───────────────────────────────────────────────────────────────────
    institutional_email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text='Institutional email address (e.g., @college.edu).',
    )
    personal_email = models.EmailField(
        blank=True,
        default='',
        validators=[EmailValidator()],
        help_text='Personal email address.',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        validators=[phone_validator],
        help_text='Primary phone number.',
    )
    alternate_phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        validators=[phone_validator],
        help_text='Secondary or guardian phone number.',
    )

    # ── Academic Profile ──────────────────────────────────────────────────────────
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='students',
        help_text='Department the student is enrolled in.',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='students',
        help_text='Academic program/course the student is enrolled in.',
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='students',
        help_text='Branch or specialization.',
    )
    current_semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name='students',
        help_text='Current semester of the student.',
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='students',
        help_text='Academic year of enrollment.',
    )
    admission_year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100),
        ],
        help_text='Year of admission, e.g., 2023.',
    )
    enrollment_date = models.DateField(
        default=timezone.now,
        help_text='Date of enrollment.',
    )

    # ── Personal Details ──────────────────────────────────────────────────────────
    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        default=GenderChoices.PREFER_NOT_TO_SAY,
        blank=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text='Date of birth.',
    )
    blood_group = models.CharField(
        max_length=10,
        choices=BloodGroupChoices.choices,
        default=BloodGroupChoices.UNKNOWN,
        blank=True,
    )
    address = models.TextField(
        blank=True,
        default='',
        help_text='Permanent or residential address.',
    )
    guardian_name = models.CharField(
        max_length=200,
        blank=True,
        default='',
        help_text="Guardian's full name.",
    )
    guardian_phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        validators=[phone_validator],
        help_text="Guardian's phone number.",
    )

    # ── Photo ─────────────────────────────────────────────────────────────────────
    photo = models.ImageField(
        upload_to='students/photos/%Y/%m/',
        null=True,
        blank=True,
        help_text='Student profile photo (used on hall tickets).',
    )

    # ── Status ───────────────────────────────────────────────────────────────────
    status = models.CharField(
        max_length=20,
        choices=StudentStatusChoices.choices,
        default=StudentStatusChoices.ACTIVE,
        db_index=True,
        help_text='Current enrollment status.',
    )
    is_eligible_for_exam = models.BooleanField(
        default=True,
        help_text='Overall exam eligibility flag. Set to False to block exam registration.',
    )
    remarks = models.TextField(
        blank=True,
        default='',
        help_text='Administrative remarks or notes about this student.',
    )

    # ── Audit Fields ─────────────────────────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students_created',
        help_text='Admin user who created this record.',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students_updated',
        help_text='Admin user who last updated this record.',
    )

    class Meta:
        db_table = 'students_student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['roll_number']
        indexes = [
            models.Index(fields=['roll_number'], name='idx_student_roll'),
            models.Index(fields=['student_id'], name='idx_student_sid'),
            models.Index(fields=['institutional_email'], name='idx_student_email'),
            models.Index(fields=['department'], name='idx_student_dept'),
            models.Index(fields=['course'], name='idx_student_course'),
            models.Index(fields=['branch'], name='idx_student_branch'),
            models.Index(fields=['current_semester'], name='idx_student_sem'),
            models.Index(fields=['academic_year'], name='idx_student_acyear'),
            models.Index(fields=['status'], name='idx_student_status'),
            models.Index(fields=['admission_year'], name='idx_student_admyear'),
            models.Index(fields=['full_name'], name='idx_student_name'),
        ]

    def __str__(self):
        return f'{self.roll_number} — {self.full_name}'

    def clean(self):
        errors = {}
        # Validate department → course relationship
        if self.department_id and self.course_id:
            if self.course.department_id != self.department_id:
                errors['course'] = (
                    f'Course "{self.course.name}" does not belong to '
                    f'department "{self.department.name}".'
                )
        # Validate course → branch relationship
        if self.branch_id and self.course_id:
            if self.branch.course_id != self.course_id:
                errors['branch'] = (
                    f'Branch "{self.branch.name}" does not belong to '
                    f'course "{self.course.name}".'
                )
        # Validate semester → course relationship
        if self.current_semester_id and self.course_id:
            if self.current_semester.course_id != self.course_id:
                errors['current_semester'] = (
                    'Selected semester does not belong to the selected course.'
                )
        # Validate date of birth
        if self.date_of_birth:
            today = timezone.now().date()
            age = (today - self.date_of_birth).days / 365
            if age < 14 or age > 80:
                errors['date_of_birth'] = 'Date of birth appears to be invalid.'
        # Validate admission year
        if self.admission_year and self.enrollment_date:
            if self.enrollment_date.year != self.admission_year:
                # Warn but don't block — some students may enroll in Jan of the next year
                pass
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Auto-populate student_id from roll_number if not provided
        if self.roll_number and not self.student_id:
            self.student_id = f"STU-{self.roll_number}"
        # Auto-populate first/last name from full_name if not provided
        if self.full_name and not self.first_name:
            parts = self.full_name.strip().split()
            if parts:
                self.first_name = parts[0]
                self.last_name = ' '.join(parts[1:]) if len(parts) > 1 else ''
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.status == StudentStatusChoices.ACTIVE

    @property
    def display_name(self):
        return self.full_name or f'{self.first_name} {self.last_name}'.strip()

    @property
    def age(self):
        if self.date_of_birth:
            today = timezone.now().date()
            return (today - self.date_of_birth).days // 365
        return None

    def deactivate(self, reason='', user=None):
        """Mark student as inactive with optional reason."""
        self.status = StudentStatusChoices.INACTIVE
        if reason:
            self.remarks = f'{self.remarks}\n[DEACTIVATED]: {reason}'.strip()
        self.updated_by = user
        self.save(update_fields=['status', 'remarks', 'updated_by', 'updated_at'])
        logger.info('Student %s deactivated by %s. Reason: %s', self.roll_number, user, reason)

    def can_register_for_exam(self):
        """Business logic check: can this student register for examinations?"""
        if self.status != StudentStatusChoices.ACTIVE:
            return False, f'Student status is {self.get_status_display()}, not Active.'
        if not self.is_eligible_for_exam:
            return False, 'Student has been marked ineligible for examinations.'
        return True, 'Eligible'

    def get_registered_subjects(self):
        """Return all active subject registrations for this student."""
        return self.subject_registrations.filter(
            status='registered'
        ).select_related('subject', 'subject__semester')

    def get_registered_exams(self):
        """Return all examination registrations for this student."""
        return self.exam_registrations.select_related(
            'exam_session', 'subject'
        )


# ─── Student Import Log ───────────────────────────────────────────────────────────
class StudentImportLog(models.Model):
    """
    Tracks the result of each CSV student import operation.
    Used for auditing and download of error reports.
    """

    class ImportStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
        PARTIAL = 'partial', 'Partial Success'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='student_import_logs',
    )
    file_name = models.CharField(max_length=255, help_text='Original filename of the CSV.')
    status = models.CharField(
        max_length=20,
        choices=ImportStatusChoices.choices,
        default=ImportStatusChoices.PENDING,
        db_index=True,
    )
    total_rows = models.PositiveIntegerField(default=0)
    successful_rows = models.PositiveIntegerField(default=0)
    failed_rows = models.PositiveIntegerField(default=0)
    duplicate_rows = models.PositiveIntegerField(default=0)
    skipped_rows = models.PositiveIntegerField(default=0)
    error_details = models.JSONField(
        default=list,
        help_text='List of row-level error dicts: {row, field, error, value}.',
    )
    summary = models.TextField(blank=True, default='')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='import_logs',
    )

    class Meta:
        db_table = 'students_import_log'
        verbose_name = 'Student Import Log'
        verbose_name_plural = 'Student Import Logs'
        ordering = ['-started_at']

    def __str__(self):
        return f'Import #{self.pk} — {self.file_name} — {self.status}'

    def mark_completed(self):
        self.status = self.ImportStatusChoices.COMPLETED
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def mark_partial(self):
        self.status = self.ImportStatusChoices.PARTIAL
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

    def mark_failed(self, error=''):
        self.status = self.ImportStatusChoices.FAILED
        self.completed_at = timezone.now()
        if error:
            self.summary = error
        self.save(update_fields=['status', 'completed_at', 'summary'])

    @property
    def success_rate(self):
        if self.total_rows == 0:
            return 0
        return round((self.successful_rows / self.total_rows) * 100, 1)


# ─── Enrollment Record ────────────────────────────────────────────────────────────
class EnrollmentRecord(models.Model):
    """
    Tracks the academic enrollment history of a student across semesters.
    Created each time a student advances to a new semester.
    """

    class EnrollmentStatusChoices(models.TextChoices):
        ENROLLED = 'enrolled', 'Enrolled'
        COMPLETED = 'completed', 'Completed'
        DETAINED = 'detained', 'Detained'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollment_records',
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name='enrollment_records',
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='enrollment_records',
    )
    status = models.CharField(
        max_length=20,
        choices=EnrollmentStatusChoices.choices,
        default=EnrollmentStatusChoices.ENROLLED,
        db_index=True,
    )
    enrolled_date = models.DateField(default=timezone.now)
    completion_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollment_records_created',
    )

    class Meta:
        db_table = 'students_enrollment_record'
        verbose_name = 'Enrollment Record'
        verbose_name_plural = 'Enrollment Records'
        ordering = ['-enrolled_date']
        unique_together = [('student', 'semester', 'academic_year')]

    def __str__(self):
        return (
            f'{self.student.roll_number} — {self.semester} '
            f'({self.academic_year.label})'
        )
