from rest_framework import serializers
from accounts.models import User
from .models import FacultyAvailability, FacultyLeave, FacultyProfile

class FacultyAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyAvailability
        fields = '__all__'

class FacultyLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyLeave
        fields = '__all__'

    def validate_faculty(self, faculty):
        request = self.context.get('request')
        if request and not request.user.is_admin:
            if faculty.user_id != request.user.pk:
                raise serializers.ValidationError('You can only request leave for your own faculty profile.')
        return faculty

class FacultyProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    availabilities = FacultyAvailabilitySerializer(many=True, read_only=True)
    leave_requests = FacultyLeaveSerializer(many=True, read_only=True)

    class Meta:
        model = FacultyProfile
        fields = ('id', 'faculty_id', 'user', 'user_name', 'department', 'designation', 'status', 'email', 'phone', 'qualification', 'specialization', 'date_of_joining', 'bio', 'availabilities', 'leave_requests', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def validate_user(self, user):
        if user.role != User.Role.FACULTY:
            raise serializers.ValidationError('A faculty profile can only be linked to a faculty account.')
        return user

    def validate_email(self, value):
        if FacultyProfile.objects.filter(email__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('This institutional email is already assigned to another faculty member.')
        return value.lower()

    def validate_faculty_id(self, value):
        if FacultyProfile.objects.filter(faculty_id__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('This faculty ID is already in use.')
        return value

class FacultyBulkDataSerializer(serializers.Serializer):
    faculty_id = serializers.CharField()
    department = serializers.CharField()
    designation = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(required=False, allow_blank=True, default='')
    status = serializers.CharField(required=False, default='ACTIVE')
