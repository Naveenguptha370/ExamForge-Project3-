from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.examinations.models import ExamSession, TimeSlot
from apps.scheduling.models import TimetableEntry
from apps.infrastructure.models import Room
from apps.students.models import Student
from apps.faculty.models import FacultyProfile

class SeatingPlan(models.Model):
    session = models.ForeignKey(ExamSession, on_delete=models.CASCADE, related_name='seating_plans')
    exam_date = models.DateField(db_index=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    total_students = models.PositiveIntegerField(default=0)
    total_rooms_used = models.PositiveIntegerField(default=0)
    spacing_rule = models.CharField(max_length=50, default='ALTERNATE_SEATS', help_text="ALTERNATE_SEATS, CROSS_DEPARTMENT")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'exam_date', 'time_slot')
        ordering = ['exam_date', 'time_slot__start_time']
        verbose_name = _('Seating Plan')
        verbose_name_plural = _('Seating Plans')

    def __str__(self):
        return f"Seating Plan for {self.exam_date} [{self.time_slot.name}] - {self.session.code}"


class RoomAllocation(models.Model):
    seating_plan = models.ForeignKey(SeatingPlan, on_delete=models.CASCADE, related_name='room_allocations')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='exam_allocations')
    allocated_count = models.PositiveIntegerField(default=0)
    primary_invigilator = models.ForeignKey(FacultyProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='room_duties')
    is_confirmed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('seating_plan', 'room')
        ordering = ['room__block__code', 'room__room_number']
        verbose_name = _('Room Allocation')
        verbose_name_plural = _('Room Allocations')

    def __str__(self):
        return f"{self.room} ({self.allocated_count} seats allocated)"


class SeatAssignment(models.Model):
    room_allocation = models.ForeignKey(RoomAllocation, on_delete=models.CASCADE, related_name='seat_assignments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assigned_seats')
    timetable_entry = models.ForeignKey(TimetableEntry, on_delete=models.CASCADE, related_name='seat_assignments')
    seat_label = models.CharField(max_length=20, help_text="e.g. A-1, B-4, R1-C2")
    row_number = models.PositiveIntegerField(default=1)
    column_number = models.PositiveIntegerField(default=1)
    desk_number = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('room_allocation', 'student')
        ordering = ['row_number', 'column_number']
        verbose_name = _('Seat Assignment')
        verbose_name_plural = _('Seat Assignments')

    def __str__(self):
        return f"{self.student.register_number} -> {self.room_allocation.room.room_number} [Seat: {self.seat_label}]"
