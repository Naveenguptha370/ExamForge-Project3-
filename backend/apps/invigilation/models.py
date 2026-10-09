from django.db import models
from apps.examinations.models import ExamSubject
from apps.infrastructure.models import ExaminationRoom
from apps.faculty.models import FacultyProfile

class InvigilatorDuty(models.Model):
    class DutyRole(models.TextChoices):
        CHIEF_SUPERINTENDENT = 'CHIEF', 'Chief Superintendent'
        HALL_INVIGILATOR = 'INVIGILATOR', 'Hall Invigilator'
        RELIEVER = 'RELIEVER', 'Reliever / Squad'

    class Status(models.TextChoices):
        ASSIGNED = 'ASSIGNED', 'Duty Assigned'
        CONFIRMED = 'CONFIRMED', 'Confirmed by Faculty'
        COMPLETED = 'COMPLETED', 'Duty Completed'
        REPLACED = 'REPLACED', 'Replaced'
        ABSENT = 'ABSENT', 'Reported Absent'

    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='invigilator_duties')
    room = models.ForeignKey(ExaminationRoom, on_delete=models.CASCADE, related_name='invigilator_duties')
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='invigilation_duties')
    duty_role = models.CharField(max_length=20, choices=DutyRole.choices, default=DutyRole.HALL_INVIGILATOR)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ASSIGNED)
    reporting_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam_subject', 'room', 'faculty')
        ordering = ['exam_subject__planned_date', 'room__room_number']

    def __str__(self):
        return f"{self.faculty.employee_id} -> {self.room.room_number} ({self.exam_subject.subject.code})"
