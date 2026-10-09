from django.db import models
from django.conf import settings
from apps.examinations.models import ExamSession, TimeSlot, ExamSubject

class Timetable(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft Schedule'
        VALIDATED = 'VALIDATED', 'Validated (Conflict-Free)'
        APPROVED = 'APPROVED', 'Approved by Controller of Examinations'
        PUBLISHED = 'PUBLISHED', 'Published to Faculty & Students'
        ARCHIVED = 'ARCHIVED', 'Archived'

    exam_session = models.OneToOneField(ExamSession, on_delete=models.CASCADE, related_name='timetable')
    version = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    total_subjects_count = models.IntegerField(default=0)
    scheduled_count = models.IntegerField(default=0)
    conflict_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_timetables')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_timetables')

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Timetable for {self.exam_session.session_code} (v{self.version}) - {self.status}"


class TimetableEntry(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='entries')
    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='timetable_entries')
    exam_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='timetable_entries')
    is_manually_adjusted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('timetable', 'exam_subject')
        ordering = ['exam_date', 'time_slot__start_time']

    def __str__(self):
        return f"{self.exam_subject.subject.code} on {self.exam_date} ({self.time_slot.name})"


class SchedulingConflict(models.Model):
    class ConflictType(models.TextChoices):
        STUDENT_CLASH = 'STUDENT_CLASH', 'Student Double-Booking'
        ROOM_OVERFLOW = 'ROOM_OVERFLOW', 'Room Capacity Overflow'
        SLOT_UNAVAILABLE = 'SLOT_UNAVAILABLE', 'Slot Unavailable'
        GAP_VIOLATION = 'GAP_VIOLATION', 'Insufficient Gap Rule'

    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='conflicts')
    conflict_type = models.CharField(max_length=30, choices=ConflictType.choices, default=ConflictType.STUDENT_CLASH)
    description = models.TextField()
    exam_subject_1 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='clashes_as_first', null=True, blank=True)
    exam_subject_2 = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='clashes_as_second', null=True, blank=True)
    affected_students_count = models.IntegerField(default=0)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_conflict_type_display()}: {self.description}"


class TimetableRevision(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.IntegerField()
    notes = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-revision_number']

    def __str__(self):
        return f"Revision {self.revision_number} for {self.timetable.exam_session.session_code}"
