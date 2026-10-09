from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, AuditLog

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'role', 'status', 'is_active', 'last_login_ip', 'date_joined')
        read_only_fields = ('id', 'date_joined', 'last_login_ip')

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('An account with this institutional email already exists.')
        return value.lower()

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate(self, attrs):
        if attrs.get('role') == User.Role.FACULTY and not attrs.get('email'):
            raise serializers.ValidationError({'email': 'Faculty accounts must have an institutional email address.'})
        return super().validate(attrs)

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'status', 'password')

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('An account with this institutional email already exists.')
        return value.lower()

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid username or password.')
        if not user.is_active:
            raise serializers.ValidationError('This account is currently inactive.')
        attrs['user'] = user
        return attrs

class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class AuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = ('id', 'actor', 'actor_name', 'action', 'model_name', 'object_id', 'details', 'ip_address', 'created_at')
        read_only_fields = fields

    def get_actor_name(self, obj):
        if obj.actor is None:
            return 'System'
        return obj.actor.get_full_name() or obj.actor.username
