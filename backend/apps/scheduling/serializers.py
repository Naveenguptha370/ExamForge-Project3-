from rest_framework import serializers
from .models import Timetable, TimetableEntry, SchedulingClash, TimetableRevision
from apps.examinations.serializers import TimeSlotSerializer, ExamSubjectConfigSerializer

class TimetableEntrySerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject_config.subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject_config.subject.name', read_only=True)
    subject_type = serializers.CharField(source='subject_config.subject.subject_type', read_only=True)
    department_id = serializers.IntegerField(source='subject_config.subject.department.id', read_only=True)
    department_name = serializers.CharField(source='subject_config.subject.department.name', read_only=True)
    department_code = serializers.CharField(source='subject_config.subject.department.code', read_only=True)
    branch_id = serializers.IntegerField(source='subject_config.subject.branch.id', read_only=True, allow_null=True)
    branch_name = serializers.CharField(source='subject_config.subject.branch.name', read_only=True, allow_null=True)
    branch_code = serializers.CharField(source='subject_config.subject.branch.code', read_only=True, allow_null=True)
    semester_number = serializers.IntegerField(source='subject_config.subject.semester_number', read_only=True)
    credits = serializers.DecimalField(source='subject_config.subject.credits', max_digits=3, decimal_places=1, read_only=True)
    difficulty = serializers.CharField(source='subject_config.subject.difficulty', read_only=True)
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    shift = serializers.CharField(source='time_slot.shift', read_only=True)
    time_range = serializers.SerializerMethodField()

    class Meta:
        model = TimetableEntry
        fields = '__all__'

    def get_time_range(self, obj):
        return f"{obj.time_slot.start_time.strftime('%I:%M %p')} - {obj.time_slot.end_time.strftime('%I:%M %p')}"


class SchedulingClashSerializer(serializers.ModelSerializer):
    subject_1_code = serializers.CharField(source='subject_1.code', read_only=True)
    subject_1_name = serializers.CharField(source='subject_1.name', read_only=True)
    subject_2_code = serializers.CharField(source='subject_2.code', read_only=True, allow_null=True)
    subject_2_name = serializers.CharField(source='subject_2.name', read_only=True, allow_null=True)
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True, allow_null=True)
    clash_type_display = serializers.CharField(source='get_clash_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = SchedulingClash
        fields = '__all__'


class TimetableRevisionSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True, allow_null=True)
    username = serializers.CharField(source='author.username', read_only=True, allow_null=True)

    class Meta:
        model = TimetableRevision
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)
    session_code = serializers.CharField(source='session.code', read_only=True)
    academic_year = serializers.CharField(source='session.academic_year', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True, allow_null=True)
    critical_clashes_count = serializers.SerializerMethodField()

    class Meta:
        model = Timetable
        fields = '__all__'

    def get_critical_clashes_count(self, obj):
        return obj.clashes.filter(severity='CRITICAL', is_resolved=False).count()


class TimetableDetailSerializer(TimetableSerializer):
    entries = TimetableEntrySerializer(many=True, read_only=True)
    clashes = SchedulingClashSerializer(many=True, read_only=True)
    revisions = TimetableRevisionSerializer(many=True, read_only=True)
