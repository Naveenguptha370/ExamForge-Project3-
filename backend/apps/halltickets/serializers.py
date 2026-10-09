from rest_framework import serializers
from .models import HallTicket

class HallTicketSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    register_number = serializers.CharField(source='student.register_number', read_only=True)
    branch_name = serializers.CharField(source='student.branch.name', read_only=True)
    branch_code = serializers.CharField(source='student.branch.code', read_only=True)
    semester_number = serializers.IntegerField(source='student.current_semester_number', read_only=True)
    session_name = serializers.CharField(source='session.name', read_only=True)
    session_code = serializers.CharField(source='session.code', read_only=True)

    class Meta:
        model = HallTicket
        fields = '__all__'
