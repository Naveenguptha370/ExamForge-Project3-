"""ExamForge M2 — Registrations Admin"""
from django.contrib import admin
from django.utils.html import format_html
from .models import SubjectRegistration, ExamRegistration, BulkRegistrationJob


@admin.register(SubjectRegistration)
class SubjectRegistrationAdmin(admin.ModelAdmin):
    list_display   = ['student_roll_display', 'student_name_display', 'subject_code_display', 'semester_number', 'academic_year', 'status_badge', 'registration_date']
    list_filter    = ['status', 'academic_year', 'subject__department']
    search_fields  = ['student__roll_number', 'student__full_name', 'subject__code', 'subject__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'registered_by', 'cancelled_by', 'cancelled_at', 'import_batch_id']
    date_hierarchy = 'registration_date'
    ordering       = ['-created_at']

    def student_roll_display(self, obj): return obj.student.roll_number if obj.student_id else '—'
    student_roll_display.short_description = 'Roll No.'

    def student_name_display(self, obj): return obj.student.full_name if obj.student_id else '—'
    student_name_display.short_description = 'Student'

    def subject_code_display(self, obj): return obj.subject.code if obj.subject_id else '—'
    subject_code_display.short_description = 'Subject'

    def status_badge(self, obj):
        colors = {'registered': '#15803D', 'confirmed': '#166534', 'cancelled': '#DC2626', 'pending': '#D97706'}
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display  = ['__str__', 'exam_session_name', 'academic_year', 'status', 'registration_date']
    list_filter   = ['status', 'academic_year']
    search_fields = ['student__roll_number', 'student__full_name', 'subject__code']
    readonly_fields = ['id', 'created_at', 'updated_at', 'registered_by', 'import_batch_id']


@admin.register(BulkRegistrationJob)
class BulkRegistrationJobAdmin(admin.ModelAdmin):
    list_display  = ['file_name', 'registration_type', 'academic_year', 'status', 'total_rows', 'successful_rows', 'failed_rows', 'created_at']
    list_filter   = ['status', 'registration_type', 'academic_year']
    readonly_fields = [f.name for f in BulkRegistrationJob._meta.fields]

    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
