from rest_framework import serializers
from .models import ExamAttendanceSheet, AttendanceRecord, AttendanceCorrectionAudit

class AttendanceCorrectionAuditSerializer(serializers.ModelSerializer):
    corrected_by_name = serializers.CharField(source='corrected_by.username', read_only=True)

    class Meta:
        model = AttendanceCorrectionAudit
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_no', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_reg = serializers.CharField(source='student.registration_no', read_only=True)
    correction_audits = AttendanceCorrectionAuditSerializer(many=True, read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = '__all__'


class ExamAttendanceSheetSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='exam_subject.subject.code', read_only=True)
    subject_name = serializers.CharField(source='exam_subject.subject.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    exam_date = serializers.DateField(source='exam_subject.planned_date', read_only=True)
    slot_name = serializers.CharField(source='exam_subject.time_slot.name', read_only=True)
    invigilator_name = serializers.CharField(source='invigilator.user.get_full_name', read_only=True)
    records = AttendanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = ExamAttendanceSheet
        fields = '__all__'
