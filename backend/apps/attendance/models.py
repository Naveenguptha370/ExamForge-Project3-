from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.examinations.models import ExamSession
from apps.scheduling.models import TimetableEntry
from apps.students.models import Student
from apps.infrastructure.models import Room
from apps.accounts.models import User

class ExamAttendanceStatus(models.TextChoices):
    PRESENT = 'PRESENT', _('Present')
    ABSENT = 'ABSENT', _('Absent')
    MALPRACTICE = 'MALPRACTICE', _('Malpractice / Debarred')
    MEDICAL_EXEMPT = 'MEDICAL_EXEMPT', _('Medical Exemption')


class AttendanceRecord(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='attendance_records')
    timetable_entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_attendance_records')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='attendance_records')
    status = models.CharField(max_length=20, choices=ExamAttendanceStatus.choices, default=ExamAttendanceStatus.PRESENT, db_index=True)
    answer_booklet_number = models.CharField(max_length=50, blank=True, default='')
    remarks = models.CharField(max_length=255, blank=True, default='')
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('timetable_entry', 'student')
        ordering = ['student__register_number']
        verbose_name = _('Attendance Record')
        verbose_name_plural = _('Attendance Records')

    def __str__(self):
        return f"{self.student.register_number} - {self.timetable_entry.subject_config.subject.code}: {self.get_status_display()}"
