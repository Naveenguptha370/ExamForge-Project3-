from django.db import models
from django.conf import settings
from apps.examinations.models import ExamSubject
from apps.infrastructure.models import ExaminationRoom
from apps.faculty.models import FacultyProfile
from apps.students.models import StudentProfile

class ExamAttendanceSheet(models.Model):
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='attendance_sheets')
    room = models.ForeignKey(ExaminationRoom, on_delete=models.CASCADE, related_name='attendance_sheets')
    invigilator = models.ForeignKey(FacultyProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_sheets')
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    total_students = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    malpractice_count = models.IntegerField(default=0)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam_subject', 'room')
        ordering = ['exam_subject__planned_date', 'room__room_number']

    def __str__(self):
        return f"Attendance: {self.exam_subject.subject.code} in {self.room.room_number}"


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        MALPRACTICE = 'MALPRACTICE', 'Booked under Malpractice'
        LATE = 'LATE', 'Permitted Late Entry'
        DEBARRED = 'DEBARRED', 'Debarred from Exam'

    sheet = models.ForeignKey(ExamAttendanceSheet, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='exam_attendance_records')
    seat_label = models.CharField(max_length=20, default='-')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PRESENT)
    answer_booklet_no = models.CharField(max_length=50, blank=True, default='')
    remarks = models.TextField(blank=True, default='')
    marked_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('sheet', 'student')
        ordering = ['student__roll_no']

    def __str__(self):
        return f"{self.student.roll_no}: {self.status} ({self.sheet.room.room_number})"


class AttendanceCorrectionAudit(models.Model):
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='correction_audits')
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    reason = models.TextField()
    corrected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Correction for {self.attendance_record.student.roll_no}: {self.previous_status} -> {self.new_status}"
