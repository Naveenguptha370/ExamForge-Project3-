"""
ExamForge M2 — Student & Academic Filters
==========================================
django-filter FilterSet classes for all M2 list endpoints.
Provides advanced filtering capabilities beyond simple search.
"""

import django_filters
from django.db.models import Q

from students.models import Student, EnrollmentRecord, StudentStatusChoices
from academics.models import (
    Department, Course, Branch, Semester, AcademicYear,
    Subject, StatusChoices, SubjectTypeChoices,
)


class StudentFilter(django_filters.FilterSet):
    """Advanced filtering for the Student list endpoint."""

    # Exact lookups
    department = django_filters.NumberFilter(field_name='department__id')
    department_code = django_filters.CharFilter(
        field_name='department__code', lookup_expr='iexact'
    )
    course = django_filters.NumberFilter(field_name='course__id')
    course_code = django_filters.CharFilter(
        field_name='course__code', lookup_expr='iexact'
    )
    branch = django_filters.NumberFilter(field_name='branch__id')
    branch_code = django_filters.CharFilter(
        field_name='branch__code', lookup_expr='iexact'
    )
    semester = django_filters.NumberFilter(field_name='current_semester__id')
    semester_number = django_filters.NumberFilter(
        field_name='current_semester__semester_number'
    )
    academic_year = django_filters.NumberFilter(field_name='academic_year__id')
    academic_year_label = django_filters.CharFilter(
        field_name='academic_year__label', lookup_expr='iexact'
    )
    status = django_filters.MultipleChoiceFilter(
        choices=StudentStatusChoices.choices
    )
    gender = django_filters.CharFilter(lookup_expr='iexact')
    is_eligible_for_exam = django_filters.BooleanFilter()

    # Range lookups
    admission_year = django_filters.NumberFilter()
    admission_year_min = django_filters.NumberFilter(
        field_name='admission_year', lookup_expr='gte'
    )
    admission_year_max = django_filters.NumberFilter(
        field_name='admission_year', lookup_expr='lte'
    )
    enrolled_after = django_filters.DateFilter(
        field_name='enrollment_date', lookup_expr='gte'
    )
    enrolled_before = django_filters.DateFilter(
        field_name='enrollment_date', lookup_expr='lte'
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    # Name search (more specific than global search)
    name_contains = django_filters.CharFilter(
        field_name='full_name', lookup_expr='icontains'
    )
    email_contains = django_filters.CharFilter(
        field_name='institutional_email', lookup_expr='icontains'
    )

    class Meta:
        model = Student
        fields = [
            'department', 'department_code',
            'course', 'course_code',
            'branch', 'branch_code',
            'semester', 'semester_number',
            'academic_year', 'academic_year_label',
            'status', 'gender',
            'is_eligible_for_exam',
            'admission_year', 'admission_year_min', 'admission_year_max',
            'enrolled_after', 'enrolled_before',
            'created_after', 'created_before',
        ]


class EnrollmentRecordFilter(django_filters.FilterSet):
    """Filtering for enrollment records."""

    student = django_filters.CharFilter(
        field_name='student__id', lookup_expr='exact'
    )
    student_roll = django_filters.CharFilter(
        field_name='student__roll_number', lookup_expr='icontains'
    )
    academic_year = django_filters.NumberFilter(field_name='academic_year__id')
    semester = django_filters.NumberFilter(field_name='semester__id')
    status = django_filters.ChoiceFilter(
        choices=EnrollmentRecord.EnrollmentStatusChoices.choices
    )

    class Meta:
        model = EnrollmentRecord
        fields = ['student', 'student_roll', 'academic_year', 'semester', 'status']


class SubjectFilter(django_filters.FilterSet):
    """Advanced filtering for the Subject list endpoint."""

    department = django_filters.NumberFilter(field_name='department__id')
    department_code = django_filters.CharFilter(
        field_name='department__code', lookup_expr='iexact'
    )
    course = django_filters.NumberFilter(field_name='course__id')
    course_code = django_filters.CharFilter(
        field_name='course__code', lookup_expr='iexact'
    )
    branch = django_filters.NumberFilter(field_name='branch__id')
    semester = django_filters.NumberFilter(field_name='semester__id')
    semester_number = django_filters.NumberFilter(
        field_name='semester__semester_number'
    )
    subject_type = django_filters.MultipleChoiceFilter(
        choices=SubjectTypeChoices.choices
    )
    status = django_filters.MultipleChoiceFilter(
        choices=StatusChoices.choices
    )
    is_external_exam = django_filters.BooleanFilter()
    is_internal_exam = django_filters.BooleanFilter()
    is_elective_group = django_filters.BooleanFilter()
    credits_min = django_filters.NumberFilter(field_name='credits', lookup_expr='gte')
    credits_max = django_filters.NumberFilter(field_name='credits', lookup_expr='lte')
    code_contains = django_filters.CharFilter(field_name='code', lookup_expr='icontains')
    name_contains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Subject
        fields = [
            'department', 'department_code',
            'course', 'course_code',
            'branch', 'semester', 'semester_number',
            'subject_type', 'status',
            'is_external_exam', 'is_internal_exam', 'is_elective_group',
            'credits_min', 'credits_max',
        ]
