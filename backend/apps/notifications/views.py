from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Announcement, InAppNotification
from .serializers import AnnouncementSerializer, InAppNotificationSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.select_related('published_by').all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user_role = self.request.user.role if hasattr(self.request.user, 'role') else 'STUDENT'
        if self.request.user.is_admin():
            return qs.filter(is_active=True)
        return qs.filter(is_active=True, target_role__in=['ALL', user_role])

    def perform_create(self, serializer):
        serializer.save(published_by=self.request.user)


class InAppNotificationViewSet(viewsets.ModelViewSet):
    queryset = InAppNotification.objects.all()
    serializer_class = InAppNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InAppNotification.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        count = InAppNotification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'message': f'Marked {count} notifications as read.'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = InAppNotification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': count})
