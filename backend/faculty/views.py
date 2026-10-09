from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import AuditLog, User
from .models import FacultyAvailability, FacultyLeave, FacultyProfile
from .serializers import FacultyAvailabilitySerializer, FacultyLeaveSerializer, FacultyProfileSerializer

class FacultyProfileViewSet(viewsets.ModelViewSet):
    queryset = FacultyProfile.objects.select_related('user').prefetch_related('availabilities', 'leave_requests').all()
    serializer_class = FacultyProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '').strip()
        department = self.request.query_params.get('department', '').strip()
        status = self.request.query_params.get('status', '').strip()
        if search:
            queryset = queryset.filter(
                Q(faculty_id__icontains=search) |
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(email__icontains=search)
            )
        if department:
            queryset = queryset.filter(department__icontains=department)
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('faculty_id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        AuditLog.objects.create(
            actor=request.user,
            action='faculty_created',
            model_name='FacultyProfile',
            object_id=str(profile.pk),
            details=f'Created faculty {profile.faculty_id}',
            ip_address=self._get_client_ip(request),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_profile = serializer.save()
        AuditLog.objects.create(
            actor=request.user,
            action='faculty_updated',
            model_name='FacultyProfile',
            object_id=str(updated_profile.pk),
            details=f'Updated faculty {updated_profile.faculty_id}',
            ip_address=self._get_client_ip(request),
        )
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def dashboard(self, request):
        profiles = FacultyProfile.objects.all()
        data = {
            'total_faculty': profiles.count(),
            'active_faculty': profiles.filter(status='ACTIVE').count(),
            'available_faculty': profiles.filter(status='ACTIVE').count(),
            'incomplete_profiles': profiles.filter(Q(email='') | Q(phone='') | Q(department='')).count(),
            'leave_requests': FacultyLeave.objects.filter(status='PENDING').count(),
            'total_workload': profiles.count() * 3,
        }
        return Response(data)

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class FacultyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = FacultyAvailability.objects.select_related('faculty').all()
    serializer_class = FacultyAvailabilitySerializer
    permission_classes = [IsAuthenticated]

class FacultyLeaveViewSet(viewsets.ModelViewSet):
    queryset = FacultyLeave.objects.select_related('faculty').all()
    serializer_class = FacultyLeaveSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        leave = serializer.save()
        AuditLog.objects.create(
            actor=request.user,
            action='faculty_leave_created',
            model_name='FacultyLeave',
            object_id=str(leave.pk),
            details=f'Leave requested for {leave.faculty.faculty_id}',
            ip_address=self._get_client_ip(request),
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
