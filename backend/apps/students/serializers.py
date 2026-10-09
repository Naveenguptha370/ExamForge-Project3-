from rest_framework import serializers
from .models import Student, StudentEnrollment, SubjectRegistration, EligibilityStatus
from apps.academics.models import Branch, Subject

class StudentSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    branch_code = serializers.CharField(source='branch.code', read_only=True)
    course_name = serializers.CharField(source='branch.course.name', read_only=True)
    department_name = serializers.CharField(source='branch.course.department.name', read_only=True)
    full_name = serializers.CharField(read_only=True)
    registered_subjects_count = serializers.IntegerField(source='subject_registrations.count', read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    register_number = serializers.CharField(source='student.register_number', read_only=True)
    semester_name = serializers.CharField(source='semester.__str__', read_only=True)

    class Meta:
        model = StudentEnrollment
        fields = '__all__'


class SubjectRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    register_number = serializers.CharField(source='student.register_number', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    branch_name = serializers.CharField(source='student.branch.name', read_only=True)
    credits = serializers.DecimalField(source='subject.credits', max_digits=3, decimal_places=1, read_only=True)

    class Meta:
        model = SubjectRegistration
        fields = '__all__'


class CSVImportPreviewSerializer(serializers.Serializer):
    csv_content = serializers.CharField(write_only=True)
    branch_id = serializers.IntegerField(required=False, allow_null=True)
