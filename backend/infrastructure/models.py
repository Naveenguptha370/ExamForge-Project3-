from django.db import models
from django.core.exceptions import ValidationError
from examinations.models import Examination


class Building(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    campus_zone = models.CharField(max_length=50, default='Main Campus')
    total_floors = models.PositiveIntegerField(default=4)
    has_elevator = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('lecture_hall', 'Lecture Hall'),
        ('exam_hall', 'Main Examination Hall'),
        ('computer_lab', 'Computer Lab'),
        ('seminar_hall', 'Seminar Hall'),
        ('drawing_hall', 'Drawing Hall'),
    ]

    room_number = models.CharField(max_length=30)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    floor = models.IntegerField(default=1)  # 0=Ground, 1=1st, etc.
    room_type = models.CharField(max_length=30, choices=ROOM_TYPE_CHOICES, default='exam_hall')
    capacity = models.PositiveIntegerField(help_text="Total physical desks/benches")
    usable_capacity = models.PositiveIntegerField(help_text="Usable capacity under safe examination seating")
    rows = models.PositiveIntegerField(default=6, help_text="Number of bench/desk rows in the room")
    columns = models.PositiveIntegerField(default=5, help_text="Number of columns/seats per row")
    
    # Accessibility and Amenities
    is_accessible = models.BooleanField(default=True, help_text="Wheelchair accessible / ramp access")
    has_cctv = models.BooleanField(default=True, help_text="Equipped with surveillance CCTV")
    has_air_conditioning = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('building', 'room_number')
        ordering = ['building__code', 'room_number']

    def clean(self):
        if self.usable_capacity > self.capacity:
            raise ValidationError({'usable_capacity': "Usable capacity cannot exceed total physical capacity."})
        if self.rows * self.columns < self.usable_capacity:
            # warn or adjust, or ensure grid can hold usable seats
            pass

    def __str__(self):
        return f"{self.building.code} - {self.room_number} ({self.usable_capacity} usable seats)"

    @property
    def display_name(self):
        return f"{self.building.name} - Room {self.room_number}"


class RoomMaintenance(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_records')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=255)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Resolved" if self.is_resolved else "Active"
        return f"Maintenance: {self.room} ({self.start_date} to {self.end_date}) [{status}]"


class RoomAssignment(models.Model):
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('active', 'Active Exam in Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    examination = models.ForeignKey(Examination, on_delete=models.CASCADE, related_name='room_assignments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='exam_assignments')
    allotted_students_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('examination', 'room')

    def __str__(self):
        return f"{self.room.display_name} -> {self.examination.subject.code} ({self.allotted_students_count} students)"
