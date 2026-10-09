from django.db import models
from apps.infrastructure.models import ExaminationRoom
from apps.examinations.models import ExamSubject
from apps.students.models import StudentProfile

class Seat(models.Model):
    room = models.ForeignKey(ExaminationRoom, on_delete=models.CASCADE, related_name='seats')
    row_num = models.IntegerField()
    col_num = models.IntegerField()
    seat_label = models.CharField(max_length=20)
    is_usable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('room', 'row_num', 'col_num')
        ordering = ['row_num', 'col_num']

    def __str__(self):
        return f"{self.room.room_number}: {self.seat_label}"


class SeatingPlan(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft Plan'
        GENERATED = 'GENERATED', 'Generated & Validated'
        LOCKED = 'LOCKED', 'Locked for Examination'

    exam_subject = models.ForeignKey(ExamSubject, on_delete=models.CASCADE, related_name='seating_plans')
    room = models.ForeignKey(ExaminationRoom, on_delete=models.CASCADE, related_name='seating_plans')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    spacing_rule = models.CharField(max_length=50, default='ALTERNATE_COLS', help_text='ALTERNATE_COLS or CHECKERBOARD')
    total_allocated = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam_subject', 'room')
        ordering = ['exam_subject__planned_date', 'room__room_number']

    def __str__(self):
        return f"Seating: {self.exam_subject.subject.code} in {self.room.room_number} ({self.total_allocated} seats)"


class SeatAllocation(models.Model):
    seating_plan = models.ForeignKey(SeatingPlan, on_delete=models.CASCADE, related_name='allocations')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='allocations')
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='seat_allocations')
    is_present = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('seating_plan', 'student'), ('seating_plan', 'seat')]
        ordering = ['seat__row_num', 'seat__col_num']

    def __str__(self):
        return f"{self.student.roll_no} -> {self.seat.seat_label} ({self.seating_plan.room.room_number})"
