from rest_framework import serializers
from .models import InvigilatorDuty

class InvigilatorDutySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.full_name', read_only=True)
    employee_id = serializers.CharField(source='faculty.employee_id', read_only=True)
    department_code = serializers.CharField(source='faculty.department.code', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True, allow_null=True)
    block_code = serializers.CharField(source='room.block.code', read_only=True, allow_null=True)
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    duty_role_display = serializers.CharField(source='get_duty_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = InvigilatorDuty
        fields = '__all__'
