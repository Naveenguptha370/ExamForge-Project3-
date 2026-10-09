from django.contrib import admin
from .models import Building, Room, RoomMaintenance, RoomAssignment


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'campus_zone', 'total_floors', 'has_elevator']
    search_fields = ['code', 'name', 'campus_zone']
    list_filter = ['campus_zone', 'has_elevator']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'building', 'floor', 'room_type', 'capacity', 'usable_capacity', 'rows', 'columns', 'is_accessible', 'is_active']
    search_fields = ['room_number', 'building__name', 'building__code']
    list_filter = ['building', 'room_type', 'floor', 'is_accessible', 'is_active', 'has_cctv']


@admin.register(RoomMaintenance)
class RoomMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['room', 'start_date', 'end_date', 'reason', 'is_resolved', 'created_at']
    list_filter = ['is_resolved', 'start_date', 'end_date']
    search_fields = ['room__room_number', 'reason']


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ['examination', 'room', 'allotted_students_count', 'status', 'assigned_at']
    list_filter = ['status', 'assigned_at']
    search_fields = ['room__room_number', 'examination__subject__code']
