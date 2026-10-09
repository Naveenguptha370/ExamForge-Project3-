from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SystemSetting
from .serializers import SystemSettingSerializer

class SystemSettingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        setting, _ = SystemSetting.objects.get_or_create(id=1)
        return Response(SystemSettingSerializer(setting).data)

    def put(self, request):
        if not request.user.is_admin():
            return Response({'error': 'Only administrators can update institutional settings.'}, status=status.HTTP_403_FORBIDDEN)
        setting, _ = SystemSetting.objects.get_or_create(id=1)
        serializer = SystemSettingSerializer(setting, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
