from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.academics.models import Branch, Semester, Subject

class StudentStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    SUSPENDED = 'SUSPENDED', _('Suspended')
    GRADUATED = 'GRADUATED', _('Graduated')
    INACTIVE = 'INACTIVE', _('Inactive / On Leave')


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='student_profile')
    register_number = models.CharField(max_length=50, unique=True, db_index=True)
    roll_number = models.CharField(max_length=50, blank=True, default='')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='students')
    current_semester_number = models.PositiveIntegerField(default=1)
    admission_year = models.CharField(max_length=10, default='2024')
    status = models.CharField(max_length=20, choices=StudentStatus.choices, default=StudentStatus.ACTIVE)
    is_eligible_for_exams = models.BooleanField(default=True)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['register_number']
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return f"{self.register_number} - {self.first_name} {self.last_name} ({self.branch.code})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class StudentEnrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='student_enrollments')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    enrolled_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'semester', 'academic_year')
        ordering = ['-academic_year', 'semester__semester_number']
        verbose_name = _('Student Enrollment')
        verbose_name_plural = _('Student Enrollments')

    def __str__(self):
        return f"{self.student.register_number} -> {self.semester}"


class EligibilityStatus(models.TextChoices):
    ELIGIBLE = 'ELIGIBLE', _('Eligible')
    LOW_ATTENDANCE = 'LOW_ATTENDANCE', _('Debarred (Low Attendance < 75%)')
    FEES_PENDING = 'FEES_PENDING', _('Hold (Fees Pending)')
    DEBARRED = 'DEBARRED', _('Debarred (Disciplinary)')


class SubjectRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_registrations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='student_registrations')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    semester_number = models.PositiveIntegerField(default=1)
    is_regular = models.BooleanField(default=True, help_text="True for regular term, False for supplementary/backlog")
    eligibility_status = models.CharField(
        max_length=30,
        choices=EligibilityStatus.choices,
        default=EligibilityStatus.ELIGIBLE
    )
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=85.0)
    is_approved = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'academic_year')
        ordering = ['student__register_number', 'subject__code']
        verbose_name = _('Subject Registration')
        verbose_name_plural = _('Subject Registrations')

    def __str__(self):
        return f"{self.student.register_number} -> {self.subject.code} ({self.eligibility_status})"

    @property
    def is_eligible(self):
        return self.eligibility_status == EligibilityStatus.ELIGIBLE and self.is_approved
