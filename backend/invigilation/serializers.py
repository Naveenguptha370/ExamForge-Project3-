from rest_framework import serializers
from .models import DutyRequirement, InvigilatorDuty
from academics.models import Faculty


class FacultySimpleSerializer(serializers.ModelSerializer):
    department_code = serializers.CharField(source='department.code', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'employee_id', 'name', 'email', 'phone', 'designation', 'department_code', 'department_name', 'max_weekly_duties', 'is_active']


class DutyRequirementSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    subject_code = serializers.CharField(source='examination.subject.code', read_only=True)

    class Meta:
        model = DutyRequirement
        fields = ['id', 'examination', 'room', 'room_number', 'building_name', 'subject_code', 'required_invigilators']


class InvigilatorDutySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    faculty_emp_id = serializers.CharField(source='faculty.employee_id', read_only=True)
    faculty_email = serializers.CharField(source='faculty.email', read_only=True)
    faculty_phone = serializers.CharField(source='faculty.phone', read_only=True)
    department_code = serializers.CharField(source='faculty.department.code', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    building_name = serializers.CharField(source='room.building.name', read_only=True)
    subject_code = serializers.CharField(source='examination.subject.code', read_only=True)
    subject_name = serializers.CharField(source='examination.subject.name', read_only=True)
    time_slot_name = serializers.CharField(source='time_slot.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = InvigilatorDuty
        fields = [
            'id', 'examination', 'room', 'room_number', 'building_name',
            'faculty', 'faculty_name', 'faculty_emp_id', 'faculty_email', 'faculty_phone',
            'department_code', 'subject_code', 'subject_name', 'duty_date',
            'time_slot', 'time_slot_name', 'role', 'role_display', 'status',
            'status_display', 'assigned_at', 'notes'
        ]
