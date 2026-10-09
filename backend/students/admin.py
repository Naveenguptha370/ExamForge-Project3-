"""ExamForge M2 — Students Admin"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Student, StudentImportLog, EnrollmentRecord


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = [
        'roll_number', 'full_name', 'department_code', 'course_code',
        'current_semester', 'status_badge', 'is_eligible_for_exam', 'admission_year',
    ]
    list_filter   = ['status', 'is_eligible_for_exam', 'department', 'course', 'academic_year']
    search_fields = ['roll_number', 'full_name', 'institutional_email', 'student_id']
    ordering      = ['department__code', 'roll_number']
    readonly_fields = [
        'id', 'student_id', 'created_at', 'updated_at',
        'created_by', 'updated_by',
    ]
    fieldsets = (
        ('Identity', {'fields': ('id', 'student_id', 'roll_number', 'full_name', 'gender', 'date_of_birth', 'blood_group')}),
        ('Academic Placement', {'fields': ('department', 'course', 'branch', 'current_semester', 'academic_year', 'admission_year', 'enrollment_date')}),
        ('Contact', {'fields': ('institutional_email', 'personal_email', 'phone', 'alternate_phone', 'address', 'guardian_name', 'guardian_phone')}),
        ('Status', {'fields': ('status', 'is_eligible_for_exam', 'remarks')}),
        ('Audit', {'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    @admin.display(description='Dept.')
    def department_code(self, obj):
        return obj.department.code if obj.department_id else '—'

    @admin.display(description='Course')
    def course_code(self, obj):
        return obj.course.code if obj.course_id else '—'

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {'active': '#15803D', 'inactive': '#6B7280', 'graduated': '#0D6940', 'suspended': '#D97706', 'withdrawn': '#DC2626'}
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px;font-size:11px;">{}</span>',
            color, obj.get_status_display()
        )


@admin.register(StudentImportLog)
class StudentImportLogAdmin(admin.ModelAdmin):
    list_display  = ['file_name', 'status', 'total_rows', 'successful_rows', 'failed_rows', 'imported_by', 'started_at']
    list_filter   = ['status']
    readonly_fields = [f.name for f in StudentImportLog._meta.fields]

    def has_add_permission(self, request):   return False
    def has_change_permission(self, request, obj=None): return False


@admin.register(EnrollmentRecord)
class EnrollmentRecordAdmin(admin.ModelAdmin):
    list_display  = ['student', 'semester', 'academic_year', 'status', 'enrolled_date']
    list_filter   = ['status', 'academic_year']
    search_fields = ['student__roll_number', 'student__full_name']
