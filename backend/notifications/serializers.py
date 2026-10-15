from rest_framework import serializers
from .models import Notification, NotificationCategory, NotificationTemplate, NotificationBatch


class NotificationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationCategory
        fields = ["id", "code", "label", "icon", "color", "is_active"]


class NotificationTemplateSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="category.label", read_only=True)
    class Meta:
        model = NotificationTemplate
        fields = ["id", "code", "category", "category_label", "channel", "subject_template",
                  "body_template", "available_variables", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]
