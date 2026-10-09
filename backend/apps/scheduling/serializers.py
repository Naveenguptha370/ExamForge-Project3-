from rest_framework import serializers
from .models import Timetable, TimetableEntry, SchedulingConflict, TimetableRevision
from apps.examinations.serializers import ExamSubjectSerializer, TimeSlotSerializer

class TimetableEntrySerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='exam_subject.subject.code', read_only=True)
    subject_name = serializers.CharField(source='exam_subject.subject.name', read_only=True)
    slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    slot_time = serializers.SerializerMethodField()
    duration_minutes = serializers.IntegerField(source='exam_subject.duration_minutes', read_only=True)
    department_name = serializers.CharField(source='exam_subject.subject.department.name', read_only=True)

    class Meta:
        model = TimetableEntry
        fields = '__all__'

    def get_slot_time(self, obj):
        return f"{obj.time_slot.start_time.strftime('%I:%M %p')} - {obj.time_slot.end_time.strftime('%I:%M %p')}"


class SchedulingConflictSerializer(serializers.ModelSerializer):
    subject_1_code = serializers.CharField(source='exam_subject_1.subject.code', read_only=True, default='')
    subject_2_code = serializers.CharField(source='exam_subject_2.subject.code', read_only=True, default='')

    class Meta:
        model = SchedulingConflict
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='exam_session.name', read_only=True)
    session_code = serializers.CharField(source='exam_session.session_code', read_only=True)
    entries = TimetableEntrySerializer(many=True, read_only=True)
    conflicts = SchedulingConflictSerializer(many=True, read_only=True)

    class Meta:
        model = Timetable
        fields = '__all__'
