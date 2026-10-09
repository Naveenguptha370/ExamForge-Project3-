"""
ExamForge M2 — Academic Management Models
==========================================
Defines the academic hierarchy:
  Department → Course → Branch → Semester → Subject
  AcademicYear (independent, referenced by student enrollment)

Design Decisions:
- All models include created_at, updated_at, created_by, status fields.
- Soft deletion via 'status' field (ACTIVE / INACTIVE / ARCHIVED).
- Protected FKs prevent accidental orphaning of related records.
- Unique constraints are at the DB level for safety.
- related_name values follow consistent <model>_<reverse> naming.

Integration Notes:
- M1 (Faculty): Department is shared; faculty belong to departments.
  M1 should FK to this Department model.
- M3 (Examinations): ExamSession references Subject and AcademicYear.
  M3 should FK to Subject and AcademicYear from this module.
- M4 (Seating): Indirectly uses Student → Branch → Course.
- M5 (Hall Tickets): References Subject, AcademicYear, and Course.
"""

import logging
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

# ─── Constants ───────────────────────────────────────────────────────────────────

class StatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    ARCHIVED = 'archived', 'Archived'


class SubjectTypeChoices(models.TextChoices):
    CORE = 'core', 'Core'
    ELECTIVE = 'elective', 'Elective'
    LAB = 'lab', 'Laboratory'
    PROJECT = 'project', 'Project'
    SEMINAR = 'seminar', 'Seminar'
    AUDIT = 'audit', 'Audit'


class CourseDurationChoices(models.IntegerChoices):
    ONE_YEAR = 1, '1 Year'
    TWO_YEARS = 2, '2 Years'
    THREE_YEARS = 3, '3 Years'
    FOUR_YEARS = 4, '4 Years'
    FIVE_YEARS = 5, '5 Years'


# ─── Code Validator ──────────────────────────────────────────────────────────────
code_validator = RegexValidator(
    regex=r'^[A-Z0-9_\-]{2,20}$',
    message='Code must be 2-20 characters, uppercase letters, digits, hyphens, or underscores only.',
    code='invalid_code',
)


# ─── Base Model ──────────────────────────────────────────────────────────────────
class AcademicBaseModel(models.Model):
    """
    Abstract base providing audit fields for all academic models.
    All M2 academic models inherit from this.
    """
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        db_index=True,
        help_text='Lifecycle status of this record.',
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_created',
        help_text='User who created this record.',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_updated',
        help_text='User who last modified this record.',
    )
    notes = models.TextField(
        blank=True,
        default='',
        help_text='Optional administrative notes.',
    )

    class Meta:
        abstract = True

    @property
    def is_active(self):
        return self.status == StatusChoices.ACTIVE

    def archive(self, user=None):
        """Soft-archive this record instead of deleting it."""
        self.status = StatusChoices.ARCHIVED
        self.updated_by = user
        self.save(update_fields=['status', 'updated_by', 'updated_at'])
        logger.info('%s #%s archived by %s', self.__class__.__name__, self.pk, user)

    def activate(self, user=None):
        """Reactivate an archived record."""
        self.status = StatusChoices.ACTIVE
        self.updated_by = user
        self.save(update_fields=['status', 'updated_by', 'updated_at'])
        logger.info('%s #%s activated by %s', self.__class__.__name__, self.pk, user)

    def deactivate(self, user=None):
        """Mark as inactive."""
        self.status = StatusChoices.INACTIVE
        self.updated_by = user
        self.save(update_fields=['status', 'updated_by', 'updated_at'])
        logger.info('%s #%s deactivated by %s', self.__class__.__name__, self.pk, user)


# ─── Academic Year ────────────────────────────────────────────────────────────────
class AcademicYear(AcademicBaseModel):
    """
    Represents an institutional academic year, e.g., 2024-2025.

    Rules:
    - End date must be after start date.
    - Only one academic year may be marked as 'is_current' at a time.
    - Label must be unique.
    - Cannot delete if students or exam sessions reference this year.
    """
    label = models.CharField(
        max_length=20,
        unique=True,
        help_text='Academic year label, e.g., "2024-2025".',
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{4}$',
                message='Label must be in the format YYYY-YYYY, e.g., 2024-2025.',
            )
        ],
    )
    start_date = models.DateField(
        help_text='First day of the academic year.',
    )
    end_date = models.DateField(
        help_text='Last day of the academic year.',
    )
    is_current = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Marks the current active academic year. Only one may be current.',
    )

    class Meta:
        db_table = 'academics_academic_year'
        verbose_name = 'Academic Year'
        verbose_name_plural = 'Academic Years'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['label'], name='idx_acyear_label'),
            models.Index(fields=['is_current'], name='idx_acyear_current'),
            models.Index(fields=['status'], name='idx_acyear_status'),
        ]

    def __str__(self):
        return self.label

    def clean(self):
        super().clean()
        if self.label and '-' in self.label and not self.start_date:
            try:
                parts = self.label.split('-')
                import datetime
                self.start_date = datetime.date(int(parts[0]), 7, 1)
                self.end_date = datetime.date(int(parts[1]), 6, 30)
            except Exception:
                pass
        errors = {}
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                errors['end_date'] = 'End date must be after the start date.'
            duration_years = (self.end_date - self.start_date).days / 365
            if duration_years < 0.5 or duration_years > 2:
                errors['end_date'] = 'Academic year duration should be between 6 months and 2 years.'
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.label and '-' in self.label and not self.start_date:
            try:
                parts = self.label.split('-')
                import datetime
                self.start_date = datetime.date(int(parts[0]), 7, 1)
                self.end_date = datetime.date(int(parts[1]), 6, 30)
            except Exception:
                pass
        self.full_clean()
        # Ensure only one academic year is marked as current
        if self.is_current:
            AcademicYear.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_current(cls):
        """Return the currently active academic year, or None."""
        return cls.objects.filter(is_current=True, status=StatusChoices.ACTIVE).first()

    @property
    def duration_months(self):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return round(delta.days / 30)
        return None

    @property
    def is_ongoing(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


# ─── Department ──────────────────────────────────────────────────────────────────
class Department(AcademicBaseModel):
    """
    Academic department within the institution.

    Shared model — M1 (Faculty) and M3 (Examinations) both reference Department.
    Do NOT duplicate this model in other apps.

    Integration:
    - M1: Faculty.department → ForeignKey(Department)
    - M3: ExamSession → references Subject → which belongs to Department
    - M4: SeatingArrangement uses Student → Course → Department
    - M5: Reports filter by Department
    """
    name = models.CharField(
        max_length=150,
        unique=True,
        help_text='Full name of the department, e.g., "Computer Science and Engineering".',
    )
    code = models.CharField(
        max_length=20,
        unique=True,
        validators=[code_validator],
        help_text='Short unique department code, e.g., "CSE".',
    )
    head_of_department = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments',
        help_text='Faculty user who is the Head of Department.',
    )
    email = models.EmailField(
        blank=True,
        default='',
        help_text='Official department email address.',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        default='',
        help_text='Department contact phone number.',
    )
    established_year = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2100),
        ],
        help_text='Year the department was established.',
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Brief description of the department.',
    )

    class Meta:
        db_table = 'academics_department'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code'], name='idx_dept_code'),
            models.Index(fields=['status'], name='idx_dept_status'),
            models.Index(fields=['name'], name='idx_dept_name'),
        ]

    def __str__(self):
        return f'{self.code} — {self.name}'

    def clean(self):
        super().clean()
        if self.name:
            self.name = self.name.strip()
        if self.code:
            self.code = self.code.strip().upper()

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.strip().upper()
        if self.name:
            self.name = self.name.strip()
        super().save(*args, **kwargs)

    @property
    def total_courses(self):
        return self.courses.filter(status=StatusChoices.ACTIVE).count()

    @property
    def total_students(self):
        return self.students.filter(status='active').count()

    @property
    def total_subjects(self):
        return self.subjects.filter(status=StatusChoices.ACTIVE).count()

    def can_be_deleted(self):
        """Check if this department can be safely deleted."""
        has_courses = self.courses.exists()
        has_students = self.students.exists()
        has_subjects = self.subjects.exists()
        return not (has_courses or has_students or has_subjects)


# ─── Course ───────────────────────────────────────────────────────────────────────
class Course(AcademicBaseModel):
    """
    Academic program or degree course, e.g., B.Tech, M.Tech, MBA.

    Belongs to a Department. Has a duration measured in years.
    A Course may have one or more Branches (specializations).
    """
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='courses',
        help_text='The department this course belongs to.',
    )
    name = models.CharField(
        max_length=200,
        help_text='Full name of the course, e.g., "Bachelor of Technology".',
    )
    code = models.CharField(
        max_length=20,
        validators=[code_validator],
        help_text='Short unique code for this course, e.g., "BTECH".',
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text='Abbreviated name, e.g., "B.Tech".',
    )
    duration_years = models.PositiveSmallIntegerField(
        choices=CourseDurationChoices.choices,
        default=CourseDurationChoices.FOUR_YEARS,
        help_text='Total duration of the course in years.',
    )
    total_semesters = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text='Total number of semesters in this course.',
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Description of the course and its objectives.',
    )
    is_postgraduate = models.BooleanField(
        default=False,
        help_text='Indicates if this is a postgraduate course.',
    )

    class Meta:
        db_table = 'academics_course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['department__code', 'name']
        unique_together = [('department', 'code')]
        indexes = [
            models.Index(fields=['code'], name='idx_course_code'),
            models.Index(fields=['department'], name='idx_course_dept'),
            models.Index(fields=['status'], name='idx_course_status'),
        ]

    def __str__(self):
        return f'{self.code} — {self.name} ({self.department.code})'

    def clean(self):
        super().clean()
        if self.code:
            self.code = self.code.strip().upper()
        if self.name:
            self.name = self.name.strip()
        # Validate total_semesters against duration_years
        expected_max = self.duration_years * 3  # max 3 semesters/year
        if self.total_semesters and self.duration_years:
            if self.total_semesters < self.duration_years:
                raise ValidationError({
                    'total_semesters': (
                        f'Total semesters ({self.total_semesters}) cannot be less than '
                        f'duration in years ({self.duration_years}).'
                    )
                })
            if self.total_semesters > expected_max:
                raise ValidationError({
                    'total_semesters': (
                        f'Total semesters ({self.total_semesters}) seems too high '
                        f'for a {self.duration_years}-year course. Maximum expected: {expected_max}.'
                    )
                })

    @property
    def total_branches(self):
        return self.branches.filter(status=StatusChoices.ACTIVE).count()

    @property
    def total_students(self):
        return self.students.filter(status='active').count()

    def can_be_deleted(self):
        has_branches = self.branches.exists()
        has_students = self.students.exists()
        has_semesters = self.semesters.exists()
        return not (has_branches or has_students or has_semesters)


# ─── Branch ───────────────────────────────────────────────────────────────────────
class Branch(AcademicBaseModel):
    """
    Specialization or branch within a course.
    Example: B.Tech → Computer Science, Electronics, Mechanical.

    A Branch belongs to a Course (and transitively to a Department).
    Branch codes are unique within a Course.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='branches',
        help_text='The course this branch belongs to.',
    )
    name = models.CharField(
        max_length=200,
        help_text='Full branch name, e.g., "Computer Science and Engineering".',
    )
    code = models.CharField(
        max_length=20,
        validators=[code_validator],
        help_text='Short unique branch code, e.g., "CSE".',
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Description of the branch.',
    )
    intake_capacity = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        help_text='Maximum annual intake for this branch.',
    )

    class Meta:
        db_table = 'academics_branch'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['course__code', 'name']
        unique_together = [('course', 'code')]
        indexes = [
            models.Index(fields=['code'], name='idx_branch_code'),
            models.Index(fields=['course'], name='idx_branch_course'),
            models.Index(fields=['status'], name='idx_branch_status'),
        ]

    def __str__(self):
        return f'{self.code} — {self.name} ({self.course.code})'

    def clean(self):
        super().clean()
        if self.code:
            self.code = self.code.strip().upper()
        if self.name:
            self.name = self.name.strip()

    @property
    def department(self):
        return self.course.department

    @property
    def total_students(self):
        return self.students.filter(status='active').count()

    def can_be_deleted(self):
        has_students = self.students.exists()
        has_semesters = self.semesters.exists()
        return not (has_students or has_semesters)


# ─── Semester ─────────────────────────────────────────────────────────────────────
class Semester(AcademicBaseModel):
    """
    Represents a single semester within a Course (and optionally a Branch).

    Important: Semester numbers are NOT globally unique — they are unique
    within a (Course, Branch) combination. e.g., B.Tech CSE has Semester 1,
    B.Tech ECE also has Semester 1.

    A Semester is the container for Subject offerings.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='semesters',
        help_text='The course this semester belongs to.',
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='semesters',
        help_text='The branch this semester belongs to, if branch-specific.',
    )
    semester_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text='Semester number, e.g., 1, 2, 3.',
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='Descriptive name, e.g., "First Semester".',
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text='Planned start date of this semester.',
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text='Planned end date of this semester.',
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='semesters',
        help_text='The academic year this semester is offered in.',
    )

    class Meta:
        db_table = 'academics_semester'
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        ordering = ['course__code', 'branch__code', 'semester_number']
        unique_together = [('course', 'branch', 'semester_number')]
        indexes = [
            models.Index(fields=['course', 'semester_number'], name='idx_sem_course_num'),
            models.Index(fields=['branch'], name='idx_sem_branch'),
            models.Index(fields=['status'], name='idx_sem_status'),
            models.Index(fields=['academic_year'], name='idx_sem_acyear'),
        ]

    def __str__(self):
        branch_part = f' / {self.branch.code}' if self.branch else ''
        return f'{self.course.code}{branch_part} — Sem {self.semester_number}'

    def clean(self):
        super().clean()
        # Validate semester number against course total_semesters
        if self.course_id and self.semester_number:
            if self.semester_number > self.course.total_semesters:
                raise ValidationError({
                    'semester_number': (
                        f'Semester number {self.semester_number} exceeds the course total '
                        f'of {self.course.total_semesters} semesters.'
                    )
                })
        # Branch must belong to the same course
        if self.branch_id and self.course_id:
            if self.branch.course_id != self.course_id:
                raise ValidationError({
                    'branch': 'Selected branch does not belong to the selected course.'
                })
        # Date validation
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({'end_date': 'End date must be after start date.'})

    @property
    def total_subjects(self):
        return self.subjects.filter(status=StatusChoices.ACTIVE).count()

    @property
    def total_enrolled_students(self):
        return self.students.filter(status='active').count()

    def can_be_deleted(self):
        has_subjects = self.subjects.exists()
        has_students = self.students.exists()
        has_registrations = self.subject_registrations.exists()
        return not (has_subjects or has_students or has_registrations)


# ─── Subject ──────────────────────────────────────────────────────────────────────
class Subject(AcademicBaseModel):
    """
    An academic subject or paper offered in a semester.

    A Subject belongs to a Department, Course, Branch, and Semester.
    The same subject code may be offered across multiple semesters
    only if the institution's rules allow it (controlled via unique constraints).

    Integration:
    - M3 (Examinations): ExamSession includes a list of Subjects.
    - M2 (Registration): SubjectRegistration references this Subject.
    - M5 (Hall Tickets): Hall ticket shows subject name and code.
    """
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='subjects',
        help_text='Department offering this subject.',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='subjects',
        help_text='Course in which this subject is taught.',
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='subjects',
        help_text='Branch for which this subject is offered (if branch-specific).',
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name='subjects',
        help_text='The semester in which this subject is offered.',
    )
    code = models.CharField(
        max_length=30,
        validators=[code_validator],
        help_text='Unique subject code, e.g., "CS301".',
    )
    name = models.CharField(
        max_length=200,
        help_text='Full subject name, e.g., "Data Structures and Algorithms".',
    )
    short_name = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text='Abbreviated subject name for display in tight spaces.',
    )
    subject_type = models.CharField(
        max_length=20,
        choices=SubjectTypeChoices.choices,
        default=SubjectTypeChoices.CORE,
        db_index=True,
        help_text='Type of subject: core, elective, lab, project, etc.',
    )
    credits = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text='Credit value for this subject.',
    )
    lecture_hours_per_week = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text='Number of lecture hours per week.',
    )
    lab_hours_per_week = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(10)],
        help_text='Number of lab hours per week.',
    )
    is_elective_group = models.BooleanField(
        default=False,
        help_text='Marks this subject as belonging to an elective group.',
    )
    elective_group_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text='Name of the elective group, if applicable.',
    )
    description = models.TextField(
        blank=True,
        default='',
        help_text='Syllabus summary or description.',
    )
    is_external_exam = models.BooleanField(
        default=True,
        help_text='Indicates if this subject has an external examination.',
    )
    is_internal_exam = models.BooleanField(
        default=True,
        help_text='Indicates if this subject has internal assessment.',
    )
    max_external_marks = models.PositiveSmallIntegerField(
        default=100,
        validators=[MaxValueValidator(500)],
        help_text='Maximum marks for external examination.',
    )
    max_internal_marks = models.PositiveSmallIntegerField(
        default=50,
        validators=[MaxValueValidator(500)],
        help_text='Maximum marks for internal assessment.',
    )
    pass_marks_external = models.PositiveSmallIntegerField(
        default=35,
        validators=[MaxValueValidator(500)],
        help_text='Minimum marks to pass external examination.',
    )

    class Meta:
        db_table = 'academics_subject'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['department__code', 'course__code', 'semester__semester_number', 'code']
        unique_together = [('course', 'branch', 'semester', 'code')]
        indexes = [
            models.Index(fields=['code'], name='idx_subject_code'),
            models.Index(fields=['department'], name='idx_subject_dept'),
            models.Index(fields=['course', 'semester'], name='idx_subject_course_sem'),
            models.Index(fields=['subject_type'], name='idx_subject_type'),
            models.Index(fields=['status'], name='idx_subject_status'),
        ]

    def __str__(self):
        return f'{self.code} — {self.name}'

    def clean(self):
        super().clean()
        if self.code:
            self.code = self.code.strip().upper()
        if self.name:
            self.name = self.name.strip()
        errors = {}
        # Validate relationships
        if self.course_id and self.department_id:
            if self.course.department_id != self.department_id:
                errors['course'] = 'Selected course does not belong to the selected department.'
        if self.branch_id and self.course_id:
            if self.branch.course_id != self.course_id:
                errors['branch'] = 'Selected branch does not belong to the selected course.'
        if self.semester_id and self.course_id:
            if self.semester.course_id != self.course_id:
                errors['semester'] = 'Selected semester does not belong to the selected course.'
        # Validate marks
        if self.pass_marks_external and self.max_external_marks:
            if self.pass_marks_external > self.max_external_marks:
                errors['pass_marks_external'] = (
                    'Pass marks cannot exceed maximum external marks.'
                )
        # Check duplicate code within course, branch and semester
        if self.course_id and self.semester_id and self.code:
            qs = Subject.objects.filter(
                course_id=self.course_id,
                branch_id=self.branch_id,
                semester_id=self.semester_id,
                code=self.code,
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                errors['code'] = f'Subject code "{self.code}" already exists for this course and semester.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.strip().upper()
        if self.name:
            self.name = self.name.strip()
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def total_marks(self):
        return self.max_external_marks + self.max_internal_marks

    @property
    def total_registered_students(self):
        return self.subject_registrations.filter(status='registered').count()

    def can_be_deleted(self):
        has_registrations = self.subject_registrations.exists()
        has_exam_registrations = self.exam_registrations.exists()
        return not (has_registrations or has_exam_registrations)

    def is_offered_for_student(self, student):
        """Check if this subject is applicable to a given student."""
        return (
            self.course_id == student.course_id
            and (self.branch_id is None or self.branch_id == student.branch_id)
            and self.semester_id == student.current_semester_id
            and self.status == StatusChoices.ACTIVE
        )
