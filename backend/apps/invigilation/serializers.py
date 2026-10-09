from rest_framework import serializers
from .models import InvigilatorDuty

class InvigilatorDutySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='faculty.employee_id', read_only=True)
    department_name = serializers.CharField(source='faculty.department.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    subject_code = serializers.CharField(source='exam_subject.subject.code', read_only=True)
    subject_name = serializers.CharField(source='exam_subject.subject.name', read_only=True)
    exam_date = serializers.DateField(source='exam_subject.planned_date', read_only=True)
    slot_name = serializers.CharField(source='exam_subject.time_slot.name', read_only=True)

    class Meta:
        model = InvigilatorDuty
        fields = '__all__'
