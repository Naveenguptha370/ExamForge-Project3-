"""
ExamForge M2 — Student Management Serializers
===============================================
DRF serializers for Student, StudentImportLog, EnrollmentRecord.

Provides list, detail, write, and import-specific serializers.
All write serializers validate cross-field relationships before saving.
"""

import logging
from rest_framework import serializers
from django.db import transaction

from students.models import Student, StudentImportLog, EnrollmentRecord, StudentStatusChoices
from academics.models import Department, Course, Branch, Semester, AcademicYear
from academics.serializers import (
    DepartmentListSerializer,
    CourseListSerializer,
    BranchListSerializer,
    SemesterListSerializer,
    AcademicYearListSerializer,
)

logger = logging.getLogger(__name__)


# ─── Student List Serializer ──────────────────────────────────────────────────────

class StudentListSerializer(serializers.ModelSerializer):
    """Compact serializer for paginated student lists."""
    department_code = serializers.CharField(source='department.code', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    branch_code = serializers.CharField(source='branch.code', read_only=True, allow_null=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True, allow_null=True)
    semester_number = serializers.IntegerField(
        source='current_semester.semester_number', read_only=True
    )
    academic_year_label = serializers.CharField(source='academic_year.label', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'roll_number', 'full_name',
            'institutional_email', 'phone',
            'department', 'department_code', 'department_name',
            'course', 'course_code', 'course_name',
            'branch', 'branch_code', 'branch_name',
            'current_semester', 'semester_number',
            'academic_year', 'academic_year_label',
            'admission_year', 'status', 'status_display',
            'is_eligible_for_exam', 'photo_url',
            'created_at', 'updated_at',
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


# ─── Student Detail Serializer ────────────────────────────────────────────────────

class StudentDetailSerializer(serializers.ModelSerializer):
    """Full student profile serializer with nested academic details."""
    department_detail = DepartmentListSerializer(source='department', read_only=True)
    course_detail = CourseListSerializer(source='course', read_only=True)
    branch_detail = BranchListSerializer(source='branch', read_only=True)
    current_semester_detail = SemesterListSerializer(source='current_semester', read_only=True)
    academic_year_detail = AcademicYearListSerializer(source='academic_year', read_only=True)
    age = serializers.ReadOnlyField()
    display_name = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    blood_group_display = serializers.CharField(source='get_blood_group_display', read_only=True)
    photo_url = serializers.SerializerMethodField()
    created_by_name = serializers.SerializerMethodField()
    updated_by_name = serializers.SerializerMethodField()
    registered_subjects_count = serializers.SerializerMethodField()
    exam_registrations_count = serializers.SerializerMethodField()
    exam_eligibility = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'roll_number',
            'full_name', 'first_name', 'last_name', 'display_name',
            'institutional_email', 'personal_email',
            'phone', 'alternate_phone',
            'department', 'department_detail',
            'course', 'course_detail',
            'branch', 'branch_detail',
            'current_semester', 'current_semester_detail',
            'academic_year', 'academic_year_detail',
            'admission_year', 'enrollment_date',
            'gender', 'gender_display',
            'date_of_birth', 'age',
            'blood_group', 'blood_group_display',
            'address', 'guardian_name', 'guardian_phone',
            'photo', 'photo_url',
            'status', 'status_display',
            'is_eligible_for_exam', 'exam_eligibility',
            'remarks',
            'registered_subjects_count', 'exam_registrations_count',
            'created_at', 'updated_at',
            'created_by_name', 'updated_by_name',
        ]
        read_only_fields = ['created_at', 'updated_at', 'student_id']

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None

    def get_updated_by_name(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return None

    def get_registered_subjects_count(self, obj):
        return obj.subject_registrations.filter(status='registered').count()

    def get_exam_registrations_count(self, obj):
        return obj.exam_registrations.filter(status='registered').count()

    def get_exam_eligibility(self, obj):
        can, reason = obj.can_register_for_exam()
        return {'eligible': can, 'reason': reason}


# ─── Student Write Serializer ─────────────────────────────────────────────────────

class StudentWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating student records."""

    class Meta:
        model = Student
        fields = [
            'roll_number', 'full_name', 'first_name', 'last_name',
            'institutional_email', 'personal_email',
            'phone', 'alternate_phone',
            'department', 'course', 'branch', 'current_semester', 'academic_year',
            'admission_year', 'enrollment_date',
            'gender', 'date_of_birth', 'blood_group',
            'address', 'guardian_name', 'guardian_phone',
            'photo', 'status', 'is_eligible_for_exam', 'remarks',
        ]
        extra_kwargs = {
            'phone': {'required': False},
            'personal_email': {'required': False},
            'branch': {'required': False},
            'date_of_birth': {'required': False},
            'address': {'required': False},
            'guardian_name': {'required': False},
            'guardian_phone': {'required': False},
            'photo': {'required': False},
        }

    def validate_roll_number(self, value):
        value = value.strip().upper()
        qs = Student.objects.filter(roll_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'A student with roll number "{value}" already exists.'
            )
        return value

    def validate_institutional_email(self, value):
        value = value.strip().lower()
        qs = Student.objects.filter(institutional_email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                f'A student with email "{value}" already exists.'
            )
        return value

    def validate(self, attrs):
        dept = attrs.get('department', getattr(self.instance, 'department', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))
        branch = attrs.get('branch', getattr(self.instance, 'branch', None))
        semester = attrs.get('current_semester', getattr(self.instance, 'current_semester', None))

        errors = {}

        if dept and course and course.department_id != dept.id:
            errors['course'] = (
                f'Course "{course.name}" does not belong to department "{dept.name}".'
            )

        if branch and course and branch.course_id != course.id:
            errors['branch'] = (
                f'Branch "{branch.name}" does not belong to course "{course.name}".'
            )

        if semester and course and semester.course_id != course.id:
            errors['current_semester'] = (
                'Selected semester does not belong to the selected course.'
            )

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
            validated_data['updated_by'] = request.user
        # Auto-generate student_id
        validated_data['student_id'] = self._generate_student_id(
            validated_data.get('department'),
            validated_data.get('admission_year'),
        )
        with transaction.atomic():
            instance = Student(**validated_data)
            instance.full_clean()
            instance.save()
        logger.info('Student created: %s — %s', instance.roll_number, instance.full_name)
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['updated_by'] = request.user
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.full_clean()
            instance.save()
        return instance

    def _generate_student_id(self, department, admission_year):
        """Generate a sequential student ID in format: DEPT-YEAR-NNNN."""
        dept_code = department.code if department else 'STU'
        year = str(admission_year)[-2:] if admission_year else '00'
        last = (
            Student.objects.filter(
                department=department,
                admission_year=admission_year,
            ).order_by('-student_id').first()
        )
        if last and last.student_id:
            try:
                seq = int(last.student_id.split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
        return f'{dept_code}-{year}-{seq:04d}'


# ─── Student Import Serializer ────────────────────────────────────────────────────

class StudentImportRowSerializer(serializers.Serializer):
    """Validates a single CSV import row before processing."""
    roll_number = serializers.CharField(max_length=20)
    full_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    department_code = serializers.CharField(max_length=20)
    course_code = serializers.CharField(max_length=20)
    branch_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    semester_number = serializers.IntegerField(min_value=1, max_value=20)
    academic_year = serializers.CharField(max_length=20)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    admission_date = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(
        choices=['male', 'female', 'other', 'prefer_not_to_say'],
        required=False,
        allow_blank=True,
    )
    date_of_birth = serializers.DateField(required=False, allow_null=True)


class StudentImportLogSerializer(serializers.ModelSerializer):
    """Serializer for import log records."""
    success_rate = serializers.ReadOnlyField()
    imported_by_name = serializers.SerializerMethodField()
    academic_year_label = serializers.CharField(source='academic_year.label', read_only=True)

    class Meta:
        model = StudentImportLog
        fields = [
            'id', 'file_name', 'status',
            'total_rows', 'successful_rows', 'failed_rows',
            'duplicate_rows', 'skipped_rows',
            'error_details', 'summary', 'success_rate',
            'imported_by_name', 'academic_year_label',
            'started_at', 'completed_at',
        ]
        read_only_fields = fields


    def get_imported_by_name(self, obj):
        if obj.imported_by:
            return obj.imported_by.get_full_name() or obj.imported_by.username
        return None


# ─── Enrollment Record Serializer ─────────────────────────────────────────────────

class EnrollmentRecordSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_number', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    semester_display = serializers.CharField(source='semester.__str__', read_only=True)
    academic_year_label = serializers.CharField(source='academic_year.label', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = EnrollmentRecord
        fields = [
            'id', 'student', 'student_roll', 'student_name',
            'semester', 'semester_display',
            'academic_year', 'academic_year_label',
            'status', 'status_display',
            'enrolled_date', 'completion_date', 'remarks',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# ─── Student Dashboard Serializer ─────────────────────────────────────────────────

class StudentDashboardSerializer(serializers.Serializer):
    """Read-only dashboard statistics serializer."""
    total_students = serializers.IntegerField()
    active_students = serializers.IntegerField()
    inactive_students = serializers.IntegerField()
    graduated_students = serializers.IntegerField()
    exam_eligible_students = serializers.IntegerField()
    students_by_department = serializers.ListField(child=serializers.DictField())
    students_by_semester = serializers.ListField(child=serializers.DictField())
    students_by_course = serializers.ListField(child=serializers.DictField())
    recent_enrollments = serializers.ListField(child=serializers.DictField())
    this_year_enrollments = serializers.IntegerField()
    import_logs_pending = serializers.IntegerField()
