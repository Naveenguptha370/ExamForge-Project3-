from django.db import models
from apps.students.models import StudentProfile
from apps.academics.models import Subject, Semester

class StudentEnrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    enrolled_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'semester', 'academic_year')
        ordering = ['-academic_year', 'semester']

    def __str__(self):
        return f"{self.student.roll_no} -> {self.semester} ({self.academic_year})"


class SubjectRegistration(models.Model):
    class EligibilityStatus(models.TextChoices):
        ELIGIBLE = 'ELIGIBLE', 'Eligible'
        ATTENDANCE_SHORTAGE = 'ATTENDANCE_SHORTAGE', 'Attendance Shortage (<75%)'
        FEES_DUE = 'FEES_DUE', 'Institutional Fees Pending'
        SUSPENDED = 'SUSPENDED', 'Disciplinary Suspension'
        DETAINED = 'DETAINED', 'Academic Detention'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='subject_registrations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='registrations')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subject_registrations')
    is_approved = models.BooleanField(default=True)
    eligibility_status = models.CharField(max_length=30, choices=EligibilityStatus.choices, default=EligibilityStatus.ELIGIBLE)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=85.0)
    internal_marks = models.DecimalField(max_digits=5, decimal_places=2, default=22.0)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject', 'semester')
        ordering = ['student', 'subject']

    def save(self, *args, **kwargs):
        # Auto compute eligibility based on min attendance rule
        if self.attendance_percentage < self.subject.min_attendance_pct:
            if self.eligibility_status == self.EligibilityStatus.ELIGIBLE:
                self.eligibility_status = self.EligibilityStatus.ATTENDANCE_SHORTAGE
        super().save(*args, **kwargs)

    def is_eligible(self):
        return self.is_approved and self.eligibility_status == self.EligibilityStatus.ELIGIBLE

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject.code} ({self.eligibility_status})"
