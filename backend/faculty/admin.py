from django.contrib import admin
from .models import FacultyAvailability, FacultyLeave, FacultyProfile

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user', 'department', 'designation', 'status', 'email', 'phone')
    search_fields = ('faculty_id', 'user__username', 'email', 'phone')

@admin.register(FacultyAvailability)
class FacultyAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'day_of_week', 'start_time', 'end_time', 'is_available')

@admin.register(FacultyLeave)
class FacultyLeaveAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'start_date', 'end_date', 'status', 'reason')
