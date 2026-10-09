from rest_framework import serializers
from .models import Department, Course, Branch, Semester, Subject

class DepartmentSerializer(serializers.ModelSerializer):
    courses_count = serializers.IntegerField(source='courses.count', read_only=True)
    subjects_count = serializers.IntegerField(source='subjects.count', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_code = serializers.CharField(source='department.code', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    department_name = serializers.CharField(source='course.department.name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    course_name = serializers.CharField(source='branch.course.name', read_only=True)

    class Meta:
        model = Semester
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True, allow_null=True)
    subject_type_display = serializers.CharField(source='get_subject_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'
