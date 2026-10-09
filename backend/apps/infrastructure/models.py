from django.db import models

class Building(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    floors_count = models.IntegerField(default=4)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.code} - {self.name}"


class ExaminationRoom(models.Model):
    class RoomType(models.TextChoices):
        LECTURE_HALL = 'LECTURE_HALL', 'Lecture Hall'
        CLASSROOM = 'CLASSROOM', 'Standard Classroom'
        DRAWING_HALL = 'DRAWING_HALL', 'Drawing Hall'
        AUDITORIUM = 'AUDITORIUM', 'Auditorium'
        SEMINAR_HALL = 'SEMINAR_HALL', 'Seminar Hall'

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        MAINTENANCE = 'MAINTENANCE', 'Under Maintenance'
        RESERVED = 'RESERVED', 'Reserved'

    room_number = models.CharField(max_length=30, unique=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms')
    floor = models.IntegerField(default=1)
    room_type = models.CharField(max_length=30, choices=RoomType.choices, default=RoomType.CLASSROOM)
    total_capacity = models.IntegerField(default=60)
    usable_capacity = models.IntegerField(default=30, help_text='Capacity after applying exam spacing')
    rows = models.IntegerField(default=5)
    columns = models.IntegerField(default=6)
    has_cctv = models.BooleanField(default=True)
    is_accessible = models.BooleanField(default=True, help_text='Wheelchair accessible')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    class Meta:
        ordering = ['building', 'room_number']

    def __str__(self):
        return f"{self.room_number} ({self.building.code}, Floor {self.floor}) - Cap: {self.usable_capacity}"


class RoomAvailability(models.Model):
    room = models.ForeignKey(ExaminationRoom, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    time_slot_name = models.CharField(max_length=50, default='Morning')
    is_available = models.BooleanField(default=True)
    reason = models.TextField(blank=True, default='')

    class Meta:
        unique_together = ('room', 'date', 'time_slot_name')
        verbose_name_plural = 'Room Availabilities'

    def __str__(self):
        return f"{self.room.room_number} on {self.date}: {'Available' if self.is_available else 'Unavailable'}"
