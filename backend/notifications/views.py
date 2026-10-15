"""
Notification API views for ExamForge.
RESTful endpoints for listing, reading, and managing user notifications.
"""
import logging
from django.utils import timezone
from rest_framework import generics, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q

from .models import Notification, NotificationCategory, NotificationPreference, NotificationBatch
from .service import notification_service

logger = logging.getLogger("examforge.notifications.views")


class NotificationSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="category.label", read_only=True)
    category_icon = serializers.CharField(source="category.icon", read_only=True)
    category_color = serializers.CharField(source="category.color", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id", "subject", "body", "is_read", "is_archived",
            "action_url", "action_label", "created_at", "read_at",
            "expires_at", "category_label", "category_icon", "category_color",
        ]
        read_only_fields = ["id", "created_at", "read_at"]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    category_code = serializers.CharField(source="category.code", read_only=True)
    category_label = serializers.CharField(source="category.label", read_only=True)

    class Meta:
        model = NotificationPreference
        fields = [
            "id", "category_code", "category_label",
            "in_app_enabled", "email_enabled", "sms_enabled", "push_enabled",
            "quiet_hours_start", "quiet_hours_end", "updated_at",
        ]
        read_only_fields = ["id", "updated_at", "category_code", "category_label"]


class NotificationListView(generics.ListAPIView):
    """
    GET /api/notifications/
    Returns paginated list of in-app notifications for the authenticated user.
    Query params:
        ?unread_only=true   — only unread
        ?category=exam      — filter by category code
        ?limit=50           — result limit (max 200)
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        unread_only = self.request.query_params.get("unread_only", "").lower() == "true"
        category = self.request.query_params.get("category", "")
        try:
            limit = min(int(self.request.query_params.get("limit", 50)), 200)
        except ValueError:
            limit = 50

        return notification_service.get_user_notifications(
            user=user,
            category_code=category or None,
            unread_only=unread_only,
            limit=limit,
        )


class NotificationDetailView(generics.RetrieveDestroyAPIView):
    """
    GET /api/notifications/<id>/   — retrieve a single notification
    DELETE /api/notifications/<id>/  — permanently delete
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.mark_read()
        return super().retrieve(request, *args, **kwargs)


class NotificationMarkReadView(APIView):
    """POST /api/notifications/<id>/read/ — mark single notification as read."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notif = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        notif.mark_read()
        return Response({"status": "read", "read_at": notif.read_at})


class NotificationMarkAllReadView(APIView):
    """POST /api/notifications/read-all/ — mark all notifications as read."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        count = notification_service.mark_all_read(request.user)
        return Response({"marked_read": count, "timestamp": timezone.now()})


class NotificationUnreadCountView(APIView):
    """GET /api/notifications/unread-count/ — lightweight badge count endpoint."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = notification_service.get_unread_count(request.user)
        return Response({"unread_count": count})


class NotificationArchiveView(APIView):
    """POST /api/notifications/archive/ — archive old notifications."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        days = int(request.data.get("days", 30))
        if days < 1 or days > 365:
            return Response({"error": "days must be between 1 and 365"}, status=400)
        archived = notification_service.archive_old(request.user, days=days)
        return Response({"archived": archived})


class NotificationPreferenceView(generics.ListAPIView):
    """GET /api/notifications/preferences/ — retrieve all preferences for current user."""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(
            user=self.request.user
        ).select_related("category").order_by("category__label")


class NotificationPreferenceUpdateView(APIView):
    """
    PATCH /api/notifications/preferences/
    Body: {"exam": {"email": false, "sms": true}, "seating": {"in_app": true}}
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        if not isinstance(request.data, dict):
            return Response({"error": "Expected a dict of {category: {channel: bool}}"}, status=400)
        updated = notification_service.update_preferences(request.user, request.data)
        return Response({
            "updated": len(updated),
            "preferences": NotificationPreferenceSerializer(updated, many=True).data,
        })


class NotificationStatsView(APIView):
    """GET /api/notifications/stats/ — per-category notification stats for the current user."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.db.models import Count, Q
        stats = Notification.objects.filter(
            recipient=request.user, is_archived=False
        ).values("category__code", "category__label").annotate(
            total=Count("id"),
            unread=Count("id", filter=Q(is_read=False)),
        ).order_by("-total")
        return Response(list(stats))


# ── Admin-only batch endpoints ──────────────────────────────────────

class BatchListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/admin/notifications/batches/  — list all batches
    POST /api/admin/notifications/batches/  — create new batch
    """
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return NotificationBatch.objects.select_related("template", "created_by").order_by("-created_at")

    def get_serializer_class(self):
        from rest_framework import serializers as s

        class BatchSerializer(s.ModelSerializer):
            success_rate = s.FloatField(read_only=True)
            class Meta:
                model = NotificationBatch
                fields = "__all__"
                read_only_fields = ["id", "created_at", "started_at", "completed_at",
                                    "sent_count", "failed_count", "success_rate"]
        return BatchSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BatchDispatchView(APIView):
    """POST /api/admin/notifications/batches/<id>/dispatch/ — trigger batch delivery."""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            batch = NotificationBatch.objects.get(pk=pk)
        except NotificationBatch.DoesNotExist:
            return Response({"error": "Batch not found"}, status=404)
        if batch.status in ("running", "completed"):
            return Response({"error": f"Batch is already {batch.status}"}, status=400)
        result = notification_service.dispatch_batch(batch)
        return Response(result)
