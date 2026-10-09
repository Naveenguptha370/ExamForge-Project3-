from rest_framework import serializers
from .models import Department, Course, Branch, Semester, Subject

class DepartmentSerializer(serializers.ModelSerializer):
    courses_count = serializers.IntegerField(source='courses.count', read_only=True)
    subjects_count = serializers.IntegerField(source='subjects.count', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class BranchSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = Branch
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    semester_label = serializers.CharField(source='semester.__str__', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Subject
        fields = '__all__'
