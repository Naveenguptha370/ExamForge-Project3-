from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Announcement, SystemNotification
from .serializers import AnnouncementSerializer, SystemNotificationSerializer
from apps.accounts.permissions import IsStaffOrAdmin

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True).order_by('-is_pinned', '-created_at')
    serializer_class = AnnouncementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)


class SystemNotificationViewSet(viewsets.ModelViewSet):
    queryset = SystemNotification.objects.all().order_by('-created_at')
    serializer_class = SystemNotificationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response({'success': True, 'message': 'Notification marked as read.'})

    @action(detail=False, methods=['post'], url_path='mark-all-read')
    def mark_all_read(self, request):
        if request.user.is_authenticated:
            self.get_queryset().update(is_read=True)
        return Response({'success': True, 'message': 'All notifications marked as read.'})
