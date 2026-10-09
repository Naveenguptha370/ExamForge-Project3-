from rest_framework import serializers
from .models import StudentEnrollment, SubjectRegistration

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_no', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    semester_name = serializers.CharField(source='semester.__str__', read_only=True)

    class Meta:
        model = StudentEnrollment
        fields = '__all__'


class SubjectRegistrationSerializer(serializers.ModelSerializer):
    student_roll = serializers.CharField(source='student.roll_no', read_only=True)
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_reg = serializers.CharField(source='student.registration_no', read_only=True)
    subject_code = serializers.CharField(source='subject.code', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    semester_name = serializers.CharField(source='semester.__str__', read_only=True)

    class Meta:
        model = SubjectRegistration
        fields = '__all__'
