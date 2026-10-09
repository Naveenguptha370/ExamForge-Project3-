from rest_framework import viewsets, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        action = self.request.query_params.get('action')
        resource = self.request.query_params.get('resource_type')
        user_id = self.request.query_params.get('user')
        if action:
            qs = qs.filter(action=action)
        if resource:
            qs = qs.filter(resource_type=resource)
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs
