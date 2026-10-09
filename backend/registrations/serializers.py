"""
ExamForge M2 — Registrations Serializers
"""
from rest_framework import serializers
from django.utils import timezone
from .models import SubjectRegistration, ExamRegistration, BulkRegistrationJob


class SubjectRegistrationSerializer(serializers.ModelSerializer):
    student_name         = serializers.ReadOnlyField()
    student_roll         = serializers.ReadOnlyField()
    subject_code         = serializers.ReadOnlyField()
    subject_name         = serializers.ReadOnlyField()
    academic_year_label  = serializers.ReadOnlyField()
    semester_number      = serializers.ReadOnlyField()
    department_code      = serializers.SerializerMethodField()
    course_code          = serializers.SerializerMethodField()
    status_display       = serializers.CharField(source='get_status_display', read_only=True)
    registered_by_username = serializers.SerializerMethodField()

    class Meta:
        model  = SubjectRegistration
        fields = [
            'id', 'student', 'subject', 'semester', 'academic_year',
            'status', 'status_display', 'registration_date',
            'student_name', 'student_roll', 'subject_code', 'subject_name',
            'department_code', 'course_code',
            'academic_year_label', 'semester_number',
            'registered_by', 'registered_by_username',
            'cancelled_at', 'cancellation_reason', 'remarks',
            'import_batch_id', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'registered_by', 'cancelled_by', 'cancelled_at',
            'import_batch_id', 'created_at', 'updated_at',
        ]

    def get_department_code(self, obj):
        try:
            return obj.student.department.code if obj.student_id else None
        except Exception:
            return None

    def get_course_code(self, obj):
        try:
            return obj.student.course.code if obj.student_id else None
        except Exception:
            return None

    def get_registered_by_username(self, obj):
        return obj.registered_by.username if obj.registered_by_id else None

    def validate(self, attrs):
        student      = attrs.get('student', getattr(self.instance, 'student', None))
        subject      = attrs.get('subject', getattr(self.instance, 'subject', None))
        academic_year = attrs.get('academic_year', getattr(self.instance, 'academic_year', None))

        if student and not student.is_eligible_for_exam:
            raise serializers.ValidationError({
                'student': f"Student {student.roll_number} is not eligible for registration."
            })
        if student and subject and academic_year:
            qs = SubjectRegistration.objects.filter(
                student=student, subject=subject, academic_year=academic_year,
                status__in=['registered', 'confirmed'],
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({
                    'subject': f"Student is already registered for {subject.code} in this academic year."
                })
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['registered_by'] = request.user
        return super().create(validated_data)


class SubjectRegistrationCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, default='Cancelled by staff', max_length=500)


class ExamRegistrationSerializer(serializers.ModelSerializer):
    student_name         = serializers.ReadOnlyField()
    student_roll         = serializers.ReadOnlyField()
    subject_code         = serializers.ReadOnlyField()
    subject_name         = serializers.ReadOnlyField()
    academic_year_label  = serializers.SerializerMethodField()
    status_display       = serializers.CharField(source='get_status_display', read_only=True)
    registered_by_username = serializers.SerializerMethodField()

    class Meta:
        model  = ExamRegistration
        fields = [
            'id', 'student', 'subject', 'academic_year',
            'exam_session_id', 'exam_session_name',
            'status', 'status_display', 'registration_date',
            'hall_ticket_number',
            'student_name', 'student_roll', 'subject_code', 'subject_name',
            'academic_year_label',
            'registered_by', 'registered_by_username',
            'cancelled_at', 'cancellation_reason', 'remarks',
            'import_batch_id', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'registered_by', 'cancelled_by', 'cancelled_at',
            'import_batch_id', 'hall_ticket_number', 'created_at', 'updated_at',
        ]

    def get_academic_year_label(self, obj):
        return str(obj.academic_year) if obj.academic_year_id else None

    def get_registered_by_username(self, obj):
        return obj.registered_by.username if obj.registered_by_id else None

    def validate(self, attrs):
        student = attrs.get('student', getattr(self.instance, 'student', None))
        if student and not student.is_eligible_for_exam:
            raise serializers.ValidationError({
                'student': f"Student {student.roll_number} is not exam eligible."
            })
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['registered_by'] = request.user
        return super().create(validated_data)


class BulkRegistrationJobSerializer(serializers.ModelSerializer):
    success_rate = serializers.ReadOnlyField()
    created_by_username = serializers.SerializerMethodField()

    class Meta:
        model  = BulkRegistrationJob
        fields = [
            'id', 'batch_id', 'registration_type', 'academic_year',
            'file_name', 'status',
            'total_rows', 'successful_rows', 'failed_rows', 'duplicate_rows',
            'success_rate', 'error_details',
            'created_by', 'created_by_username',
            'started_at', 'completed_at', 'created_at',
        ]
        read_only_fields = fields

    def get_created_by_username(self, obj):
        return obj.created_by.username if obj.created_by_id else None


class AvailableSubjectSerializer(serializers.Serializer):
    """Read-only serializer for listing subjects available to a student."""
    id               = serializers.UUIDField()
    code             = serializers.CharField()
    name             = serializers.CharField()
    subject_type     = serializers.CharField()
    credits          = serializers.DecimalField(max_digits=4, decimal_places=1)
    is_external_exam = serializers.BooleanField()
    is_internal_exam = serializers.BooleanField()
    max_external_marks = serializers.IntegerField()
    max_internal_marks = serializers.IntegerField()
    semester_number  = serializers.IntegerField(source='semester.semester_number', default=None)
    already_registered = serializers.BooleanField(default=False)
