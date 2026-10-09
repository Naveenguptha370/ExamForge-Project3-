from rest_framework import serializers
from .models import Announcement, InAppNotification

class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='published_by.username', read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'


class InAppNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppNotification
        fields = '__all__'
