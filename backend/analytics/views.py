"""
Analytics API views for ExamForge.
Provides dashboard, trend, department, health, and activity endpoints
for the institutional governance portal.
"""
import logging
from datetime import date, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics, serializers
from django.db.models import Count, Q
from django.utils import timezone

from .models import AnalyticsSnapshot, DepartmentMetric, SystemHealthLog, UserActivityLog
from .service import analytics_service

logger = logging.getLogger("examforge.analytics.views")


class DashboardSummaryView(APIView):
    """
    GET /api/analytics/dashboard/
    Returns comprehensive institutional KPI summary for the admin dashboard.
    Accessible by admin and superuser roles only.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        summary = analytics_service.get_dashboard_summary()
        return Response(summary)


class SnapshotListView(generics.ListAPIView):
    """
    GET /api/analytics/snapshots/?period=daily&days=30
    Returns paginated list of analytics snapshots.
    """
    permission_classes = [IsAdminUser]

    class SnapshotSerializer(serializers.ModelSerializer):
        registration_approval_rate = serializers.FloatField(read_only=True)
        hall_utilization_rate = serializers.FloatField(read_only=True)

        class Meta:
            model = AnalyticsSnapshot
            fields = "__all__"

    serializer_class = SnapshotSerializer

    def get_queryset(self):
        period = self.request.query_params.get("period", "daily")
        days = int(self.request.query_params.get("days", 30))
        cutoff = date.today() - timedelta(days=days)
        return AnalyticsSnapshot.objects.filter(
            period=period, date__gte=cutoff
        ).order_by("-date")


class TrendView(APIView):
    """
    GET /api/analytics/trends/?metric=registrations&days=30
    Returns day-by-day trend data for a specified metric.
    Available metrics: registrations, students, seats_allocated, hall_tickets
    """
    permission_classes = [IsAdminUser]

    VALID_METRICS = {
        "registrations": "total_registrations",
        "students": "total_students",
        "seats": "seats_allocated",
        "duties": "invigilation_duties",
    }

    def get(self, request):
        metric_key = request.query_params.get("metric", "registrations")
        days = min(int(request.query_params.get("days", 30)), 180)

        field = self.VALID_METRICS.get(metric_key)
        if not field:
            return Response({"error": f"Unknown metric. Valid: {list(self.VALID_METRICS)}"}, status=400)

        cutoff = date.today() - timedelta(days=days)
        snapshots = AnalyticsSnapshot.objects.filter(
            period="daily", date__gte=cutoff
        ).order_by("date").values("date", field)

        return Response({
            "metric": metric_key,
            "field": field,
            "period_days": days,
            "data": [{"date": str(s["date"]), "value": s[field]} for s in snapshots],
        })


class DepartmentMetricView(APIView):
    """
    GET /api/analytics/departments/?snapshot_date=2026-10-15
    Returns per-department metrics for a specific snapshot date.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        snapshot_date_str = request.query_params.get("snapshot_date", str(date.today()))
        try:
            snapshot_date = date.fromisoformat(snapshot_date_str)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        try:
            snapshot = AnalyticsSnapshot.objects.get(period="daily", date=snapshot_date)
        except AnalyticsSnapshot.DoesNotExist:
            return Response({"error": f"No snapshot found for {snapshot_date}"}, status=404)

        metrics = DepartmentMetric.objects.filter(snapshot=snapshot).values(
            "department_code", "department_name", "student_count",
            "registered_count", "seated_count", "faculty_count",
            "invigilation_duties_count", "absent_count"
        ).order_by("department_name")

        data = []
        for m in metrics:
            m["registration_rate"] = (
                round(m["registered_count"] / m["student_count"] * 100, 2)
                if m["student_count"] > 0 else 0.0
            )
            data.append(m)

        return Response({"snapshot_date": str(snapshot_date), "departments": data})


class SystemHealthView(APIView):
    """
    GET /api/analytics/health/     — latest health status
    POST /api/analytics/health/    — trigger a new health probe
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        hours = int(request.query_params.get("hours", 24))
        history = analytics_service.get_health_history(hours=hours)
        try:
            latest = SystemHealthLog.objects.latest()
            current_status = latest.status
        except SystemHealthLog.DoesNotExist:
            current_status = "unknown"

        return Response({
            "current_status": current_status,
            "checked_period_hours": hours,
            "history": history,
        })

    def post(self, request):
        log = analytics_service.record_health_check()
        return Response({
            "status": log.status,
            "db_response_ms": log.db_response_ms,
            "timestamp": log.timestamp,
        })


class UserActivityView(APIView):
    """
    GET /api/analytics/activity/?user_id=<id>&days=30
    Returns activity breakdown for a specific user.
    Admin access only.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_id = request.query_params.get("user_id")
        days = int(request.query_params.get("days", 30))

        if not user_id:
            return Response({"error": "user_id is required"}, status=400)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        summary = analytics_service.get_activity_summary(user, days=days)
        return Response(summary)


class RecordSnapshotView(APIView):
    """
    POST /api/analytics/snapshots/record/
    Manually trigger snapshot recording for today (or a specified date).
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        date_str = request.data.get("date")
        target_date = None
        if date_str:
            try:
                target_date = date.fromisoformat(date_str)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        snapshot = analytics_service.record_daily_snapshot(target_date)
        return Response({
            "snapshot_id": snapshot.id,
            "date": str(snapshot.date),
            "total_students": snapshot.total_students,
            "total_registrations": snapshot.total_registrations,
            "seats_allocated": snapshot.seats_allocated,
        })
