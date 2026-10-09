from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FacultyProfile, FacultyAvailability, FacultyLeave, FacultyStatus
from .serializers import (
    FacultyProfileSerializer, FacultyAvailabilitySerializer,
    FacultyLeaveSerializer
)
from apps.accounts.permissions import IsAdminUserRole, IsStaffOrAdmin

class FacultyProfileViewSet(viewsets.ModelViewSet):
    queryset = FacultyProfile.objects.all().order_by('department__name', 'first_name')
    serializer_class = FacultyProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'department__name']
    ordering_fields = ['first_name', 'department__name', 'designation', 'current_duties_count']

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get('department')
        status_val = self.request.query_params.get('status')
        eligible = self.request.query_params.get('is_eligible')

        if dept:
            qs = qs.filter(department_id=dept)
        if status_val:
            qs = qs.filter(status=status_val)
        if eligible is not None:
            qs = qs.filter(is_eligible_for_invigilation=eligible.lower() == 'true')
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]


class FacultyAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = FacultyAvailability.objects.all().order_by('date')
    serializer_class = FacultyAvailabilitySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        faculty = self.request.query_params.get('faculty')
        date = self.request.query_params.get('date')
        if faculty:
            qs = qs.filter(faculty_id=faculty)
        if date:
            qs = qs.filter(date=date)
        return qs

    def get_permissions(self):
        return [IsAuthenticated()]


class FacultyLeaveViewSet(viewsets.ModelViewSet):
    queryset = FacultyLeave.objects.all().order_by('-start_date')
    serializer_class = FacultyLeaveSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        faculty = self.request.query_params.get('faculty')
        if faculty:
            qs = qs.filter(faculty_id=faculty)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]
