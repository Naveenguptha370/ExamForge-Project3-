from rest_framework import serializers
from .models import FacultyProfile, FacultyAvailability, FacultyLeave
from apps.accounts.serializers import UserSerializer

class FacultyProfileSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = FacultyProfile
        fields = '__all__'


class FacultyAvailabilitySerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)

    class Meta:
        model = FacultyAvailability
        fields = '__all__'


class FacultyLeaveSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='faculty.employee_id', read_only=True)

    class Meta:
        model = FacultyLeave
        fields = '__all__'
