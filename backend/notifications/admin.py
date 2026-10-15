"""
Django admin configuration for the ExamForge Notifications app.
Provides full CRUD, inline editing, and bulk action support.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Q

from .models import (
    Notification, NotificationCategory, NotificationTemplate,
    NotificationQueue, NotificationPreference, NotificationBatch,
)
from .service import notification_service


@admin.register(NotificationCategory)
class NotificationCategoryAdmin(admin.ModelAdmin):
    list_display = ["code", "label", "icon", "color_preview", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["code", "label"]
    ordering = ["label"]

    def color_preview(self, obj):
        return format_html(
            '<span style="display:inline-block;width:16px;height:16px;'
            'background:{};border:1px solid #ccc;vertical-align:middle;"></span> {}',
            obj.color, obj.color
        )
    color_preview.short_description = "Color"


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ["code", "category", "channel", "is_active", "created_at"]
    list_filter = ["channel", "is_active", "category"]
    search_fields = ["code", "subject_template"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["code"]
    fieldsets = [
        ("Identity", {"fields": ["code", "category", "channel", "is_active"]}),
        ("Content", {"fields": ["subject_template", "body_template", "available_variables"]}),
        ("Settings", {"fields": ["requires_confirmation"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["subject_short", "recipient", "category", "is_read", "created_at", "expires_at"]
    list_filter = ["is_read", "is_archived", "category"]
    search_fields = ["subject", "body", "recipient__email"]
    readonly_fields = ["id", "created_at", "read_at"]
    date_hierarchy = "created_at"
    ordering = ["-created_at"]
    actions = ["mark_selected_read", "archive_selected"]

    def subject_short(self, obj):
        return obj.subject[:60] + ("..." if len(obj.subject) > 60 else "")
    subject_short.short_description = "Subject"

    @admin.action(description="Mark selected notifications as read")
    def mark_selected_read(self, request, queryset):
        updated = queryset.filter(is_read=False).update(is_read=True, read_at=timezone.now())
        self.message_user(request, f"{updated} notifications marked as read.")

    @admin.action(description="Archive selected notifications")
    def archive_selected(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(request, f"{updated} notifications archived.")


@admin.register(NotificationQueue)
class NotificationQueueAdmin(admin.ModelAdmin):
    list_display = ["subject_short", "recipient", "channel", "status", "priority", "scheduled_at"]
    list_filter = ["status", "channel", "priority"]
    search_fields = ["subject", "recipient__email"]
    readonly_fields = ["id", "created_at", "sent_at"]
    ordering = ["priority", "scheduled_at"]
    actions = ["retry_failed"]

    def subject_short(self, obj):
        return obj.subject[:60]
    subject_short.short_description = "Subject"

    @admin.action(description="Retry failed notifications")
    def retry_failed(self, request, queryset):
        updated = queryset.filter(status="failed").update(status="pending", retry_count=0)
        self.message_user(request, f"{updated} notifications re-queued.")


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "in_app_enabled", "email_enabled", "sms_enabled"]
    list_filter = ["category", "in_app_enabled", "email_enabled"]
    search_fields = ["user__email"]
    ordering = ["user", "category"]


class BatchInline(admin.TabularInline):
    model = NotificationBatch
    extra = 0
    readonly_fields = ["id", "status", "total_recipients", "sent_count", "failed_count"]
    fields = ["id", "title", "status", "total_recipients", "sent_count", "failed_count"]
    can_delete = False


@admin.register(NotificationBatch)
class NotificationBatchAdmin(admin.ModelAdmin):
    list_display = ["title", "template", "status", "total_recipients", "sent_count",
                    "failed_count", "success_rate_display", "created_by", "created_at"]
    list_filter = ["status"]
    search_fields = ["title"]
    readonly_fields = ["id", "created_at", "started_at", "completed_at",
                       "sent_count", "failed_count", "total_recipients"]
    ordering = ["-created_at"]
    actions = ["dispatch_selected"]

    def success_rate_display(self, obj):
        rate = obj.success_rate
        color = "#2D6A4F" if rate >= 95 else ("#F59E0B" if rate >= 80 else "#EF4444")
        return format_html('<span style="color:{};font-weight:bold;">{}%</span>', color, rate)
    success_rate_display.short_description = "Success Rate"

    @admin.action(description="Dispatch selected batches")
    def dispatch_selected(self, request, queryset):
        sent_total = 0
        for batch in queryset.filter(status__in=["draft", "scheduled"]):
            result = notification_service.dispatch_batch(batch)
            sent_total += result["sent"]
        self.message_user(request, f"Dispatched. Total sent: {sent_total}.")
