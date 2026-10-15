from django.contrib import admin
from django.utils.html import format_html
from .models import AnalyticsSnapshot, DepartmentMetric, SystemHealthLog, UserActivityLog


class DepartmentMetricInline(admin.TabularInline):
    model = DepartmentMetric
    extra = 0
    readonly_fields = ["department_code", "department_name", "student_count", "faculty_count"]
    can_delete = False


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ["date", "period", "total_students", "total_registrations",
                    "seats_allocated", "invigilation_duties", "created_at"]
    list_filter = ["period"]
    date_hierarchy = "date"
    readonly_fields = ["created_at"]
    inlines = [DepartmentMetricInline]


@admin.register(SystemHealthLog)
class SystemHealthLogAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "status_display", "db_response_ms", "pending_notifications"]
    list_filter = ["status"]
    date_hierarchy = "timestamp"
    readonly_fields = ["timestamp"]

    def status_display(self, obj):
        colors = {"healthy": "#2D6A4F", "degraded": "#F59E0B", "critical": "#EF4444"}
        color = colors.get(obj.status, "#888")
        return format_html('<span style="color:{};font-weight:bold;">{}</span>', color, obj.get_status_display())
    status_display.short_description = "Status"


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "resource_type", "resource_id", "timestamp"]
    list_filter = ["action", "resource_type"]
    search_fields = ["user__email", "resource_id"]
    readonly_fields = ["timestamp"]
    date_hierarchy = "timestamp"
