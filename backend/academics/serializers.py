"""
ExamForge M2 — Academic Management Serializers
================================================
DRF serializers for Department, Course, Branch,
Semester, AcademicYear, and Subject.

All write serializers include cross-field validation.
Read serializers include nested relationship summaries.
"""

import logging
from rest_framework import serializers
from django.db import transaction

from academics.models import (
    Department,
    Course,
    Branch,
    Semester,
    AcademicYear,
    Subject,
    StatusChoices,
    SubjectTypeChoices,
)

logger = logging.getLogger(__name__)


# ─── Academic Year Serializers ────────────────────────────────────────────────────

class AcademicYearListSerializer(serializers.ModelSerializer):
    """Compact serializer for dropdown lists."""

    class Meta:
        model = AcademicYear
        fields = ['id', 'label', 'start_date', 'end_date', 'is_current', 'status']


class AcademicYearDetailSerializer(serializers.ModelSerializer):
    """Full serializer including computed fields."""
    duration_months = serializers.ReadOnlyField()
    is_ongoing = serializers.ReadOnlyField()
    total_semesters = serializers.SerializerMethodField()
    total_students = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()

    class Meta:
        model = AcademicYear
        fields = [
            'id', 'label', 'start_date', 'end_date', 'is_current', 'status',
            'duration_months', 'is_ongoing',
            'total_semesters', 'total_students',
            'notes', 'created_at', 'updated_at',
            'created_by_name', 'updated_by_name',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_total_semesters(self, obj):
        return obj.semesters.count()

    def get_total_students(self, obj):
        return obj.students.filter(status='active').count()

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None

    def get_updated_by_name(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return None


class AcademicYearWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating academic years."""

    class Meta:
        model = AcademicYear
        fields = [
            'label', 'start_date', 'end_date', 'is_current', 'status', 'notes',
        ]

    def validate(self, attrs):
        start = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        if start and end:
            if end <= start:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date.'
                })
        return attrs

    def validate_label(self, value):
        import re
        if not re.match(r'^\d{4}-\d{4}$', value):
            raise serializers.ValidationError(
                'Label must be in YYYY-YYYY format, e.g., 2024-2025.'
            )
        parts = value.split('-')
        if int(parts[1]) != int(parts[0]) + 1:
            raise serializers.ValidationError(
                'Academic year must span exactly one year, e.g., 2024-2025.'
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        with transaction.atomic():
            instance = super().create(validated_data)
        logger.info('AcademicYear created: %s by %s', instance.label, validated_data.get('created_by'))
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        with transaction.atomic():
            instance = super().update(instance, validated_data)
        return instance


# ─── Department Serializers ───────────────────────────────────────────────────────

class DepartmentListSerializer(serializers.ModelSerializer):
    """Compact serializer for department lists and dropdowns."""
    total_courses = serializers.ReadOnlyField()
    total_students = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = [
            'id', 'code', 'name', 'status',
            'total_courses', 'total_students',
        ]


class DepartmentDetailSerializer(serializers.ModelSerializer):
    """Full department serializer with computed summaries."""
    total_courses = serializers.ReadOnlyField()
    total_students = serializers.ReadOnlyField()
    total_subjects = serializers.ReadOnlyField()
    can_be_deleted = serializers.ReadOnlyField()
    head_name = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'code', 'name', 'email', 'phone',
            'established_year', 'description', 'status',
            'head_of_department', 'head_name',
            'total_courses', 'total_students', 'total_subjects',
            'can_be_deleted',
            'notes', 'created_at', 'updated_at', 'created_by_name',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_head_name(self, obj):
        if obj.head_of_department:
            return (
                obj.head_of_department.get_full_name()
                or obj.head_of_department.username
            )
        return None

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None


class DepartmentWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating departments."""

    class Meta:
        model = Department
        fields = [
            'code', 'name', 'email', 'phone',
            'established_year', 'description', 'status',
            'head_of_department', 'notes',
        ]

    def validate_code(self, value):
        value = value.strip().upper()
        qs = Department.objects.filter(code=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'Department with code "{value}" already exists.'
            )
        return value

    def validate_name(self, value):
        value = value.strip()
        qs = Department.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'Department with name "{value}" already exists.'
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        instance = super().create(validated_data)
        logger.info('Department created: %s — %s', instance.code, instance.name)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


# ─── Course Serializers ───────────────────────────────────────────────────────────

class CourseListSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    total_branches = serializers.ReadOnlyField()
    total_students = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'short_name',
            'department', 'department_code', 'department_name',
            'duration_years', 'total_semesters',
            'is_postgraduate', 'status',
            'total_branches', 'total_students',
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    department_detail = DepartmentListSerializer(source='department', read_only=True)
    total_branches = serializers.ReadOnlyField()
    total_students = serializers.ReadOnlyField()
    can_be_deleted = serializers.ReadOnlyField()
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'code', 'name', 'short_name',
            'department', 'department_detail',
            'duration_years', 'total_semesters',
            'is_postgraduate', 'description', 'status',
            'total_branches', 'total_students', 'can_be_deleted',
            'notes', 'created_at', 'updated_at', 'created_by_name',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None


class CourseWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'department', 'code', 'name', 'short_name',
            'duration_years', 'total_semesters',
            'is_postgraduate', 'description', 'status', 'notes',
        ]

    def validate(self, attrs):
        duration = attrs.get('duration_years', getattr(self.instance, 'duration_years', None))
        total_sem = attrs.get('total_semesters', getattr(self.instance, 'total_semesters', None))
        if duration and total_sem:
            if total_sem < duration:
                raise serializers.ValidationError({
                    'total_semesters': (
                        f'Total semesters ({total_sem}) cannot be less than '
                        f'duration years ({duration}).'
                    )
                })
        return attrs

    def validate_code(self, value):
        value = value.strip().upper()
        department_id = self.initial_data.get('department')
        if department_id:
            qs = Course.objects.filter(department_id=department_id, code=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    f'A course with code "{value}" already exists in this department.'
                )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        instance = super().create(validated_data)
        logger.info('Course created: %s — %s', instance.code, instance.name)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


# ─── Branch Serializers ───────────────────────────────────────────────────────────

class BranchListSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    department_code = serializers.CharField(source='course.department.code', read_only=True)
    total_students = serializers.ReadOnlyField()

    class Meta:
        model = Branch
        fields = [
            'id', 'code', 'name',
            'course', 'course_code', 'course_name', 'department_code',
            'intake_capacity', 'status', 'total_students',
        ]


class BranchDetailSerializer(serializers.ModelSerializer):
    course_detail = CourseListSerializer(source='course', read_only=True)
    total_students = serializers.ReadOnlyField()
    can_be_deleted = serializers.ReadOnlyField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = [
            'id', 'code', 'name', 'description',
            'course', 'course_detail', 'department',
            'intake_capacity', 'status',
            'total_students', 'can_be_deleted',
            'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_department(self, obj):
        dept = obj.department
        return {'id': dept.id, 'code': dept.code, 'name': dept.name}


class BranchWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branch
        fields = [
            'course', 'code', 'name', 'description',
            'intake_capacity', 'status', 'notes',
        ]

    def validate_code(self, value):
        value = value.strip().upper()
        course_id = self.initial_data.get('course')
        if course_id:
            qs = Branch.objects.filter(course_id=course_id, code=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    f'A branch with code "{value}" already exists in this course.'
                )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


# ─── Semester Serializers ─────────────────────────────────────────────────────────

class SemesterListSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    branch_code = serializers.CharField(source='branch.code', read_only=True, allow_null=True)
    total_subjects = serializers.ReadOnlyField()
    total_enrolled_students = serializers.ReadOnlyField()

    class Meta:
        model = Semester
        fields = [
            'id', 'semester_number', 'name',
            'course', 'course_code', 'branch', 'branch_code',
            'academic_year', 'start_date', 'end_date', 'status',
            'total_subjects', 'total_enrolled_students',
        ]


class SemesterDetailSerializer(serializers.ModelSerializer):
    course_detail = CourseListSerializer(source='course', read_only=True)
    branch_detail = BranchListSerializer(source='branch', read_only=True)
    academic_year_label = serializers.CharField(source='academic_year.label', read_only=True)
    total_subjects = serializers.ReadOnlyField()
    total_enrolled_students = serializers.ReadOnlyField()
    can_be_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Semester
        fields = [
            'id', 'semester_number', 'name',
            'course', 'course_detail',
            'branch', 'branch_detail',
            'academic_year', 'academic_year_label',
            'start_date', 'end_date', 'status',
            'total_subjects', 'total_enrolled_students', 'can_be_deleted',
            'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class SemesterWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = [
            'course', 'branch', 'semester_number', 'name',
            'academic_year', 'start_date', 'end_date', 'status', 'notes',
        ]

    def validate(self, attrs):
        course = attrs.get('course', getattr(self.instance, 'course', None))
        branch = attrs.get('branch', getattr(self.instance, 'branch', None))
        sem_num = attrs.get('semester_number', getattr(self.instance, 'semester_number', None))
        start = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end = attrs.get('end_date', getattr(self.instance, 'end_date', None))

        # Branch must belong to course
        if branch and course and branch.course_id != course.id:
            raise serializers.ValidationError({
                'branch': 'Selected branch does not belong to the selected course.'
            })
        # Semester number must not exceed course total
        if course and sem_num and sem_num > course.total_semesters:
            raise serializers.ValidationError({
                'semester_number': (
                    f'Semester number {sem_num} exceeds course total of '
                    f'{course.total_semesters} semesters.'
                )
            })
        # Date validation
        if start and end and end <= start:
            raise serializers.ValidationError({'end_date': 'End date must be after start date.'})
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


# ─── Subject Serializers ──────────────────────────────────────────────────────────

class SubjectListSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    branch_code = serializers.CharField(source='branch.code', read_only=True, allow_null=True)
    semester_number = serializers.IntegerField(source='semester.semester_number', read_only=True)
    total_registered_students = serializers.ReadOnlyField()

    class Meta:
        model = Subject
        fields = [
            'id', 'code', 'name', 'short_name',
            'department', 'department_code',
            'course', 'course_code',
            'branch', 'branch_code',
            'semester', 'semester_number',
            'subject_type', 'credits', 'status',
            'is_external_exam', 'is_internal_exam',
            'total_registered_students',
        ]


class SubjectDetailSerializer(serializers.ModelSerializer):
    department_detail = DepartmentListSerializer(source='department', read_only=True)
    course_detail = CourseListSerializer(source='course', read_only=True)
    branch_detail = BranchListSerializer(source='branch', read_only=True)
    semester_detail = SemesterListSerializer(source='semester', read_only=True)
    total_marks = serializers.ReadOnlyField()
    total_registered_students = serializers.ReadOnlyField()
    can_be_deleted = serializers.ReadOnlyField()

    class Meta:
        model = Subject
        fields = [
            'id', 'code', 'name', 'short_name', 'description',
            'department', 'department_detail',
            'course', 'course_detail',
            'branch', 'branch_detail',
            'semester', 'semester_detail',
            'subject_type', 'credits',
            'lecture_hours_per_week', 'lab_hours_per_week',
            'is_elective_group', 'elective_group_name',
            'is_external_exam', 'is_internal_exam',
            'max_external_marks', 'max_internal_marks',
            'pass_marks_external', 'total_marks',
            'status', 'total_registered_students', 'can_be_deleted',
            'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class SubjectWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = [
            'department', 'course', 'branch', 'semester',
            'code', 'name', 'short_name', 'description',
            'subject_type', 'credits',
            'lecture_hours_per_week', 'lab_hours_per_week',
            'is_elective_group', 'elective_group_name',
            'is_external_exam', 'is_internal_exam',
            'max_external_marks', 'max_internal_marks',
            'pass_marks_external', 'status', 'notes',
        ]

    def validate(self, attrs):
        dept = attrs.get('department', getattr(self.instance, 'department', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))
        branch = attrs.get('branch', getattr(self.instance, 'branch', None))
        semester = attrs.get('semester', getattr(self.instance, 'semester', None))

        if dept and course and course.department_id != dept.id:
            raise serializers.ValidationError({
                'course': 'Course does not belong to the selected department.'
            })
        if branch and course and branch.course_id != course.id:
            raise serializers.ValidationError({
                'branch': 'Branch does not belong to the selected course.'
            })
        if semester and course and semester.course_id != course.id:
            raise serializers.ValidationError({
                'semester': 'Semester does not belong to the selected course.'
            })
        # Validate marks
        max_ext = attrs.get('max_external_marks', getattr(self.instance, 'max_external_marks', 100))
        pass_ext = attrs.get('pass_marks_external', getattr(self.instance, 'pass_marks_external', 35))
        if max_ext and pass_ext and pass_ext > max_ext:
            raise serializers.ValidationError({
                'pass_marks_external': 'Pass marks cannot exceed maximum external marks.'
            })
        return attrs

    def validate_code(self, value):
        return value.strip().upper()

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        instance = super().create(validated_data)
        logger.info('Subject created: %s — %s', instance.code, instance.name)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        return super().update(instance, validated_data)


# ─── Academic Dashboard Serializer ───────────────────────────────────────────────

class AcademicDashboardSerializer(serializers.Serializer):
    """Read-only summary for the Academic Management dashboard."""
    total_departments = serializers.IntegerField()
    active_departments = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    active_courses = serializers.IntegerField()
    total_branches = serializers.IntegerField()
    total_semesters = serializers.IntegerField()
    total_subjects = serializers.IntegerField()
    active_subjects = serializers.IntegerField()
    total_academic_years = serializers.IntegerField()
    current_academic_year = AcademicYearListSerializer(allow_null=True)
    subjects_by_type = serializers.DictField(child=serializers.IntegerField())
    departments_summary = serializers.ListField(child=serializers.DictField())
