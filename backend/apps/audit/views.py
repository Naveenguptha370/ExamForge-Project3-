from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog, SystemSetting
from .serializers import AuditLogSerializer, SystemSettingSerializer
from apps.accounts.permissions import IsAdminUserRole

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['action', 'resource_type', 'user__username', 'resource_id']
    permission_classes = [IsAdminUserRole]

    def get_queryset(self):
        qs = super().get_queryset()
        action_val = self.request.query_params.get('action')
        resource = self.request.query_params.get('resource_type')
        user_id = self.request.query_params.get('user')
        if action_val:
            qs = qs.filter(action=action_val)
        if resource:
            qs = qs.filter(resource_type=resource)
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs


class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all().order_by('key')
    serializer_class = SystemSettingSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]
