from rest_framework import serializers
from .models import FacultyProfile, FacultyAvailability, FacultyLeave

class FacultyProfileSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    full_name = serializers.CharField(read_only=True)
    designation_display = serializers.CharField(source='get_designation_display', read_only=True)
    assigned_duties_count = serializers.IntegerField(source='invigilator_duties.count', read_only=True)

    class Meta:
        model = FacultyProfile
        fields = '__all__'


class FacultyAvailabilitySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.full_name', read_only=True)
    department_code = serializers.CharField(source='faculty.department.code', read_only=True)

    class Meta:
        model = FacultyAvailability
        fields = '__all__'


class FacultyLeaveSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.full_name', read_only=True)

    class Meta:
        model = FacultyLeave
        fields = '__all__'
