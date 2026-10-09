from rest_framework import serializers
from .models import Announcement, SystemNotification

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True, allow_null=True)
    target_role_display = serializers.CharField(source='get_target_role_display', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'


class SystemNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemNotification
        fields = '__all__'
