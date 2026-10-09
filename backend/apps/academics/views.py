from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Department, Course, Branch, Semester, Subject
from .serializers import (
    DepartmentSerializer, CourseSerializer, BranchSerializer,
    SemesterSerializer, SubjectSerializer
)
from apps.accounts.permissions import IsAdminUserRole, IsStaffOrAdmin

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'head_of_department']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('code')
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'department__name']

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get('department')
        if dept:
            qs = qs.filter(department_id=dept)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by('code')
    serializer_class = BranchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'name', 'course__name']

    def get_queryset(self):
        qs = super().get_queryset()
        course = self.request.query_params.get('course')
        if course:
            qs = qs.filter(course_id=course)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all().order_by('semester_number')
    serializer_class = SemesterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        branch = self.request.query_params.get('branch')
        year = self.request.query_params.get('academic_year')
        if branch:
            qs = qs.filter(branch_id=branch)
        if year:
            qs = qs.filter(academic_year=year)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all().order_by('code')
    serializer_class = SubjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'department__name']
    ordering_fields = ['code', 'name', 'semester_number', 'credits']

    def get_queryset(self):
        qs = super().get_queryset()
        dept = self.request.query_params.get('department')
        branch = self.request.query_params.get('branch')
        sem = self.request.query_params.get('semester_number')
        sub_type = self.request.query_params.get('subject_type')
        if dept:
            qs = qs.filter(department_id=dept)
        if branch:
            qs = qs.filter(branch_id=branch)
        if sem:
            qs = qs.filter(semester_number=sem)
        if sub_type:
            qs = qs.filter(subject_type=sub_type)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUserRole()]
        return [IsAuthenticated()]
