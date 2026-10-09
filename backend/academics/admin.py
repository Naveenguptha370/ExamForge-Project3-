"""ExamForge M2 — Academics Admin"""
from django.contrib import admin
from django.utils.html import format_html
from .models import AcademicYear, Department, Course, Branch, Semester, Subject


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display  = ['label', 'start_date', 'end_date', 'is_current', 'status', 'total_semesters']
    list_filter   = ['status', 'is_current']
    search_fields = ['label']

    @admin.display(description='Semesters')
    def total_semesters(self, obj):
        return obj.semesters.count()


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display  = ['code', 'name', 'email', 'phone', 'established_year', 'status', 'course_count', 'student_count']
    list_filter   = ['status']
    search_fields = ['code', 'name', 'email']
    ordering      = ['code']

    @admin.display(description='Courses')
    def course_count(self, obj):
        return obj.courses.filter(status='active').count()

    @admin.display(description='Students')
    def student_count(self, obj):
        return obj.students.filter(status='active').count()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ['code', 'name', 'department', 'duration_years', 'total_semesters', 'is_postgraduate', 'status']
    list_filter   = ['status', 'department', 'is_postgraduate']
    search_fields = ['code', 'name']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display  = ['code', 'name', 'course', 'intake_capacity', 'status']
    list_filter   = ['status', 'course__department']
    search_fields = ['code', 'name']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display  = ['semester_number', 'name', 'course', 'branch', 'academic_year', 'status', 'subject_count']
    list_filter   = ['status', 'course__department', 'academic_year']
    search_fields = ['name', 'course__code']

    @admin.display(description='Subjects')
    def subject_count(self, obj):
        return obj.subjects.filter(status='active').count()


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ['code', 'name', 'department', 'course', 'semester', 'subject_type', 'credits', 'is_external_exam', 'status']
    list_filter   = ['status', 'subject_type', 'department', 'is_external_exam', 'is_elective_group']
    search_fields = ['code', 'name', 'short_name']
    ordering      = ['department__code', 'semester__semester_number', 'code']
