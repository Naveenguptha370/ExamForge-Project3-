from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FacultyProfile, FacultyAvailability, FacultyLeave
from .serializers import FacultyProfileSerializer, FacultyAvailabilitySerializer, FacultyLeaveSerializer

class FacultyProfileViewSet(viewsets.ModelViewSet):
    queryset = FacultyProfile.objects.select_related('user', 'department').all()
    serializer_class = FacultyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get('department')
        designation = self.request.query_params.get('designation')
        search = self.request.query_params.get('search')
        is_available = self.request.query_params.get('is_available')

        if dept:
            qs = qs.filter(department_id=dept)
        if designation:
            qs = qs.filter(designation=designation)
        if search:
            qs = qs.filter(employee_id__icontains=search) | qs.filter(user__first_name__icontains=search) | qs.filter(user__last_name__icontains=search) | qs.filter(user__email__icontains=search)
        if is_available is not None:
            qs = qs.filter(is_available_for_duty=is_available.lower() == 'true')
        return qs

    @action(detail=False, methods=['get'])
    def summary(self, request):
        total = FacultyProfile.objects.count()
        available = FacultyProfile.objects.filter(is_available_for_duty=True).count()
        pending_leaves = FacultyLeave.objects.filter(status='PENDING').count()
        return Response({
            'total_faculty': total,
            'available_faculty': available,
            'unavailable_faculty': total - available,
            'pending_leaves': pending_leaves
        })


class FacultyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = FacultyAvailability.objects.select_related('faculty__user').all()
    serializer_class = FacultyAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        faculty_id = self.request.query_params.get('faculty')
        date = self.request.query_params.get('date')
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)
        if date:
            qs = qs.filter(date=date)
        return qs


class FacultyLeaveViewSet(viewsets.ModelViewSet):
    queryset = FacultyLeave.objects.select_related('faculty__user', 'approved_by').all().order_by('-created_at')
    serializer_class = FacultyLeaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        leave.status = FacultyLeave.Status.APPROVED
        leave.approved_by = request.user
        leave.save()
        return Response({'status': 'Leave approved successfully'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = FacultyLeave.Status.REJECTED
        leave.approved_by = request.user
        leave.save()
        return Response({'status': 'Leave rejected'})
