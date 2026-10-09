from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.examinations.models import ExamSession, TimeSlot
from apps.faculty.models import FacultyProfile
from apps.infrastructure.models import Room

class DutyRole(models.TextChoices):
    CHIEF_SUPERINTENDENT = 'CHIEF_SUPERINTENDENT', _('Chief Superintendent')
    HALL_INVIGILATOR = 'HALL_INVIGILATOR', _('Hall Invigilator')
    RELIEVER = 'RELIEVER', _('Relieving Invigilator')
    SQUAD_MEMBER = 'SQUAD_MEMBER', _('Flying Squad Officer')


class DutyStatus(models.TextChoices):
    ASSIGNED = 'ASSIGNED', _('Assigned')
    CONFIRMED = 'CONFIRMED', _('Confirmed by Faculty')
    COMPLETED = 'COMPLETED', _('Duty Completed')
    ABSENT = 'ABSENT', _('Absent / Reassigned')


class InvigilatorDuty(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='invigilator_duties')
    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='invigilator_duties')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='duty_invigilators')
    exam_date = models.DateField(db_index=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    duty_role = models.CharField(max_length=30, choices=DutyRole.choices, default=DutyRole.HALL_INVIGILATOR)
    status = models.CharField(max_length=20, choices=DutyStatus.choices, default=DutyStatus.ASSIGNED)
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('faculty', 'exam_date', 'time_slot')
        ordering = ['exam_date', 'time_slot__start_time', 'faculty__first_name']
        verbose_name = _('Invigilator Duty')
        verbose_name_plural = _('Invigilator Duties')

    def __str__(self):
        return f"{self.faculty.full_name} -> {self.room.room_number if self.room else 'Squad'} on {self.exam_date} [{self.time_slot.name}]"
