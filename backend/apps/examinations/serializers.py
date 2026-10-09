from rest_framework import serializers
from .models import (
    ExamSession, TimeSlot, ExamSubjectConfig,
    SchedulingConstraintConfig, ExamSessionHistory, SessionStatus
)
from apps.academics.serializers import SubjectSerializer, DepartmentSerializer

class TimeSlotSerializer(serializers.ModelSerializer):
    shift_display = serializers.CharField(source='get_shift_display', read_only=True)
    time_range_formatted = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = '__all__'

    def get_time_range_formatted(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"


class ExamSubjectConfigSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    department_name = serializers.CharField(source='subject.department.name', read_only=True)
    branch_name = serializers.CharField(source='subject.branch.name', read_only=True, allow_null=True)
    semester_number = serializers.IntegerField(source='subject.semester_number', read_only=True)
    credits = serializers.DecimalField(source='subject.credits', max_digits=3, decimal_places=1, read_only=True)
    preferred_slot_name = serializers.CharField(source='preferred_slot.name', read_only=True, allow_null=True)

    class Meta:
        model = ExamSubjectConfig
        fields = '__all__'


class SchedulingConstraintConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchedulingConstraintConfig
        fields = '__all__'


class ExamSessionHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, allow_null=True)

    class Meta:
        model = ExamSessionHistory
        fields = '__all__'


class ExamSessionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    total_subjects_count = serializers.IntegerField(source='configured_subjects.count', read_only=True)
    has_timetable = serializers.SerializerMethodField()
    is_published = serializers.BooleanField(read_only=True)
    is_locked = serializers.BooleanField(read_only=True)

    class Meta:
        model = ExamSession
        fields = '__all__'

    def get_has_timetable(self, obj):
        return hasattr(obj, 'timetable') and obj.timetable is not None


class ExamSessionDetailSerializer(ExamSessionSerializer):
    configured_subjects = ExamSubjectConfigSerializer(many=True, read_only=True)
    constraint_config = SchedulingConstraintConfigSerializer(read_only=True)
    history_logs = ExamSessionHistorySerializer(many=True, read_only=True)
