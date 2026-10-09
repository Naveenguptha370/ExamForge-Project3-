from django.contrib import admin
from .models import InvigilatorDuty


@admin.register(InvigilatorDuty)
class InvigilatorDutyAdmin(admin.ModelAdmin):
    list_display = ['faculty', 'room', 'exam_subject', 'duty_role', 'status', 'reporting_time', 'assigned_at']
    list_filter = ['duty_role', 'status', 'reporting_time']
    search_fields = ['faculty__employee_id', 'faculty__user__first_name', 'faculty__user__last_name', 'room__room_number']
