from django.contrib import admin
from .models import Seat, SeatingPlan, SeatAllocation


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['seat_label', 'room', 'row_num', 'col_num', 'is_usable']
    list_filter = ['is_usable', 'room__building']
    search_fields = ['seat_label', 'room__room_number']


@admin.register(SeatingPlan)
class SeatingPlanAdmin(admin.ModelAdmin):
    list_display = ['exam_subject', 'room', 'status', 'spacing_rule', 'total_allocated', 'updated_at']
    list_filter = ['status', 'spacing_rule']
    search_fields = ['exam_subject__subject__code', 'room__room_number']


@admin.register(SeatAllocation)
class SeatAllocationAdmin(admin.ModelAdmin):
    list_display = ['seating_plan', 'seat', 'student', 'is_present', 'is_locked']
    list_filter = ['is_present', 'is_locked']
    search_fields = ['student__roll_no', 'seat__seat_label', 'seating_plan__room__room_number']
