from rest_framework import serializers
from .models import AttendanceRecord

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    register_number = serializers.CharField(source='student.register_number', read_only=True)
    roll_number = serializers.CharField(source='student.roll_number', read_only=True)
    branch_name = serializers.CharField(source='student.branch.name', read_only=True)
    subject_code = serializers.CharField(source='timetable_entry.subject_config.subject.code', read_only=True)
    subject_name = serializers.CharField(source='timetable_entry.subject_config.subject.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'
