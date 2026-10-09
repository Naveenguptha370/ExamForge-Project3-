from rest_framework import serializers
from .models import HallTicket, HallTicketEntry

class HallTicketEntrySerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='exam_subject.subject.code', read_only=True)
    subject_name = serializers.CharField(source='exam_subject.subject.name', read_only=True)

    class Meta:
        model = HallTicketEntry
        fields = '__all__'


class HallTicketSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_no', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_reg = serializers.CharField(source='student.registration_no', read_only=True)
    department_name = serializers.CharField(source='student.department.name', read_only=True)
    session_name = serializers.CharField(source='exam_session.name', read_only=True)
    session_code = serializers.CharField(source='exam_session.session_code', read_only=True)
    entries = HallTicketEntrySerializer(many=True, read_only=True)

    class Meta:
        model = HallTicket
        fields = '__all__'
