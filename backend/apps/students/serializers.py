from rest_framework import serializers
from .models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True, default='')
    semester_number = serializers.IntegerField(source='semester.number', read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
