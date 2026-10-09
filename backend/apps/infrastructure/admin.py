from django.contrib import admin
from .models import Building, ExaminationRoom, RoomAvailability


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'floors_count']
    search_fields = ['code', 'name']


@admin.register(ExaminationRoom)
class ExaminationRoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'building', 'floor', 'room_type', 'total_capacity', 'usable_capacity', 'rows', 'columns', 'is_accessible', 'status']
    search_fields = ['room_number', 'building__name', 'building__code']
    list_filter = ['building', 'room_type', 'floor', 'is_accessible', 'status', 'has_cctv']


@admin.register(RoomAvailability)
class RoomAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['room', 'date', 'time_slot_name', 'is_available']
    list_filter = ['is_available', 'date', 'time_slot_name']
    search_fields = ['room__room_number']
