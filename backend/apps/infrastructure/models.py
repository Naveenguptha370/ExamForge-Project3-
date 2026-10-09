from django.db import models
from django.utils.translation import gettext_lazy as _

class Block(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    total_floors = models.PositiveIntegerField(default=4)
    campus_zone = models.CharField(max_length=50, blank=True, default='North Wing')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']
        verbose_name = _('Academic Block')
        verbose_name_plural = _('Academic Blocks')

    def __str__(self):
        return f"{self.code} - {self.name}"


class RoomType(models.TextChoices):
    EXAM_HALL = 'EXAM_HALL', _('Examination Hall')
    CLASSROOM = 'CLASSROOM', _('Standard Classroom')
    COMPUTER_LAB = 'COMPUTER_LAB', _('Computer Lab / Digital Hall')
    DRAWING_HALL = 'DRAWING_HALL', _('Engineering Drawing Hall')
    AUDITORIUM = 'AUDITORIUM', _('Auditorium / Seminar Hall')


class Room(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50, db_index=True)
    floor_number = models.PositiveIntegerField(default=1)
    room_type = models.CharField(max_length=30, choices=RoomType.choices, default=RoomType.CLASSROOM)
    rows_count = models.PositiveIntegerField(default=6)
    columns_count = models.PositiveIntegerField(default=6)
    total_capacity = models.PositiveIntegerField(default=36)
    usable_exam_capacity = models.PositiveIntegerField(default=30)
    has_cctv = models.BooleanField(default=True)
    is_accessible = models.BooleanField(default=True)
    has_power_backup = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('block', 'room_number')
        ordering = ['block__code', 'room_number']
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return f"{self.block.code}-{self.room_number} ({self.get_room_type_display()}, Cap: {self.usable_exam_capacity})"


class RoomAvailability(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField(db_index=True)
    slot_shift = models.CharField(max_length=20, default='FULL_DAY')
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        unique_together = ('room', 'date', 'slot_shift')
        ordering = ['date', 'room__room_number']
        verbose_name = _('Room Availability')
        verbose_name_plural = _('Room Availabilities')

    def __str__(self):
        status = "Available" if self.is_available else f"Occupied/Maintenance ({self.reason})"
        return f"{self.room} on {self.date} [{self.slot_shift}]: {status}"
