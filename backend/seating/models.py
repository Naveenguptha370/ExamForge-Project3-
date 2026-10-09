from django.db import models
from examinations.models import Examination
from infrastructure.models import Room
from academics.models import Student


class SeatingPlan(models.Model):
    SPACING_CHOICES = [
        ('consecutive', 'Standard Consecutive (Dense)'),
        ('alternate_gap', 'Alternate Seat Gap (50% Density)'),
        ('checkerboard', 'Checkerboard Diagonal Pattern'),
        ('department_separated', 'Cross-Department Separation (Anti-Cheating)'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft Plan'),
        ('generated', 'Generated Automatically'),
        ('validated', 'Validated & Conflict-Free'),
        ('approved', 'Approved & Published'),
        ('archived', 'Archived')
    ]

    examination = models.OneToOneField(Examination, on_delete=models.CASCADE, related_name='seating_plan')
    session_title = models.CharField(max_length=200, blank=True, default='')
    spacing_rule = models.CharField(max_length=30, choices=SPACING_CHOICES, default='department_separated')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_allocated = models.PositiveIntegerField(default=0)
    total_unallocated = models.PositiveIntegerField(default=0)
    capacity_shortage = models.PositiveIntegerField(default=0)
    validation_status = models.CharField(max_length=50, default='Pending')
    validation_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Seating Plan: {self.examination.subject.code} ({self.get_spacing_rule_display()}) - {self.total_allocated} seated"


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    row_index = models.PositiveIntegerField(help_text="1-indexed row number")
    col_index = models.PositiveIntegerField(help_text="1-indexed column number")
    seat_label = models.CharField(max_length=20, help_text="e.g. A1, A2 or R1-C1")
    is_usable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('room', 'row_index', 'col_index')
        ordering = ['room', 'row_index', 'col_index']

    def __str__(self):
        return f"{self.room.room_number}: {self.seat_label}"


class SeatAllocation(models.Model):
    ALLOCATION_TYPE_CHOICES = [
        ('auto', 'Automatic Engine Allocation'),
        ('manual_swap', 'Manual Seat Adjustment / Swap'),
        ('special_accommodation', 'Special Accessibility Accommodation'),
    ]

    seating_plan = models.ForeignKey(SeatingPlan, on_delete=models.CASCADE, related_name='allocations')
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='seat_allocations')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='seat_allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seat_allocations')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True, blank=True, related_name='allocations')
    seat_label = models.CharField(max_length=20)
    allocation_type = models.CharField(max_length=30, choices=ALLOCATION_TYPE_CHOICES, default='auto')
    allocated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Enforce that no student has multiple seats for the same examination
        unique_together = [
            ('examination', 'student'),
            ('examination', 'room', 'seat'),
        ]
        ordering = ['room', 'seat__row_index', 'seat__col_index']

    def __str__(self):
        return f"{self.student.roll_no} -> {self.room.room_number} [{self.seat_label}] ({self.examination.subject.code})"
