from rest_framework import serializers
from .models import ExamSession, TimeSlot, ExamSubject
from apps.academics.serializers import SubjectSerializer

class TimeSlotSerializer(serializers.ModelSerializer):
    formatted_time = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = '__all__'

    def get_formatted_time(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"


class ExamSubjectSerializer(serializers.ModelSerializer):
    subject_details = SubjectSerializer(source='subject', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    slot_time = serializers.SerializerMethodField()

    class Meta:
        model = ExamSubject
        fields = '__all__'

    def get_slot_time(self, obj):
        if obj.time_slot:
            return f"{obj.time_slot.start_time.strftime('%I:%M %p')} - {obj.time_slot.end_time.strftime('%I:%M %p')}"
        return None


class ExamSessionSerializer(serializers.ModelSerializer):
    subjects_count = serializers.IntegerField(source='exam_subjects.count', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ExamSession
        fields = '__all__'
