from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='user.username', read_only=True, default='System')
    actor_role = serializers.CharField(source='user.role', read_only=True, default='SYSTEM')

    class Meta:
        model = AuditLog
        fields = '__all__'
