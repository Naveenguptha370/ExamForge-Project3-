from rest_framework import serializers
from .models import AuditLog, SystemSetting

class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    user_fullname = serializers.CharField(source='user.get_full_name', read_only=True, allow_null=True)

    class Meta:
        model = AuditLog
        fields = '__all__'


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = '__all__'
