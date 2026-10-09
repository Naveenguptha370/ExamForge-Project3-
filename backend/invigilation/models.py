from django.db import models
from django.core.exceptions import ValidationError
from examinations.models import Examination, TimeSlot
from infrastructure.models import Room
from academics.models import Faculty


class DutyRequirement(models.Model):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='invigilation_requirements')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='invigilation_requirements')
    required_invigilators = models.PositiveIntegerField(default=1, help_text="Number of faculty needed (e.g. 1 per 25 students)")

    class Meta:
        unique_together = ('examination', 'room')

    def __str__(self):
        return f"{self.examination.subject.code} - {self.room.room_number}: {self.required_invigilators} invigilators"


class InvigilatorDuty(models.Model):
    ROLE_CHOICES = [
        ('chief_superintendent', 'Chief Invigilator / Superintendent'),
        ('hall_invigilator', 'Hall Invigilator'),
        ('reliever_squad', 'Reliever / Flying Squad'),
    ]

    STATUS_CHOICES = [
        ('assigned', 'Assigned & Confirmed'),
        ('reassigned', 'Reassigned Manually'),
        ('completed', 'Duty Completed'),
        ('absent', 'Reported Absent / Replaced'),
    ]

    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='invigilator_duties')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='invigilator_duties')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='invigilator_duties')
    duty_date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='invigilator_duties')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='hall_invigilator')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        # Prevent same faculty being assigned to multiple rooms for the same examination/timeslot
        unique_together = [
            ('examination', 'room', 'faculty'),
            ('duty_date', 'time_slot', 'faculty'),
        ]
        ordering = ['duty_date', 'time_slot__start_time', 'room__room_number']

    def clean(self):
        # Overlap check
        overlap = InvigilatorDuty.objects.filter(
            duty_date=self.duty_date,
            time_slot=self.time_slot,
            faculty=self.faculty
        ).exclude(pk=self.pk).exists()
        if overlap:
            raise ValidationError(f"Faculty {self.faculty.name} is already assigned to another examination during this time slot!")

    def __str__(self):
        return f"{self.faculty.name} -> {self.room.room_number} [{self.duty_date} {self.time_slot.name}]"
