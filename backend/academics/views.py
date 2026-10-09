"""
ExamForge M2 — Academic Management Views
==========================================
ViewSets for Department, Course, Branch, Semester,
AcademicYear, and Subject management.
"""

import logging
from django.db.models import Q, Count
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from academics.models import (
    Department, Course, Branch, Semester, AcademicYear, Subject, StatusChoices
)
from academics.serializers import (
    DepartmentListSerializer, DepartmentDetailSerializer, DepartmentWriteSerializer,
    CourseListSerializer, CourseDetailSerializer, CourseWriteSerializer,
    BranchListSerializer, BranchDetailSerializer, BranchWriteSerializer,
    SemesterListSerializer, SemesterDetailSerializer, SemesterWriteSerializer,
    AcademicYearListSerializer, AcademicYearDetailSerializer, AcademicYearWriteSerializer,
    SubjectListSerializer, SubjectDetailSerializer, SubjectWriteSerializer,
    AcademicDashboardSerializer,
)
from academics.services import AcademicService
from students.permissions import IsAdminOrExamStaff, IsAdminOrExamStaffOrReadOnly
from config.pagination import StandardResultsPagination

logger = logging.getLogger(__name__)


class AcademicYearViewSet(viewsets.ModelViewSet):
    """
    GET    /api/v1/academics/years/
    POST   /api/v1/academics/years/
    GET    /api/v1/academics/years/{id}/
    PATCH  /api/v1/academics/years/{id}/
    DELETE /api/v1/academics/years/{id}/
    GET    /api/v1/academics/years/current/   → Current active academic year
    POST   /api/v1/academics/years/{id}/set-current/ → Mark as current
    """
    queryset = AcademicYear.objects.all().order_by('-start_date')
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['label']
    ordering_fields = ['label', 'start_date', 'end_date', 'is_current']
    ordering = ['-start_date']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AcademicYearWriteSerializer
        if self.action == 'list':
            return AcademicYearListSerializer
        return AcademicYearDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'set_current']:
            return [IsAuthenticated(), IsAdminOrExamStaff()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'status': 'success', 'message': f'Academic year "{instance.label}" created.', 'data': AcademicYearDetailSerializer(instance).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.students.exists() or instance.semesters.exists():
            return Response(
                {'status': 'error', 'message': 'Cannot delete an academic year with associated students or semesters. Archive it instead.'},
                status=status.HTTP_409_CONFLICT,
            )
        instance.delete()
        return Response({'status': 'success', 'message': 'Academic year deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='current')
    def current(self, request):
        year = AcademicYear.get_current()
        if not year:
            return Response({'status': 'success', 'data': None, 'message': 'No current academic year set.'})
        return Response({'status': 'success', 'data': AcademicYearDetailSerializer(year).data})

    @action(detail=True, methods=['post'], url_path='set-current')
    def set_current(self, request, pk=None):
        instance = self.get_object()
        AcademicYear.objects.filter(is_current=True).update(is_current=False)
        instance.is_current = True
        instance.save(update_fields=['is_current'])
        return Response({'status': 'success', 'message': f'"{instance.label}" is now the current academic year.'})


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Department management.
    GET    /api/v1/academics/departments/
    POST   /api/v1/academics/departments/
    GET    /api/v1/academics/departments/{id}/
    PATCH  /api/v1/academics/departments/{id}/
    DELETE /api/v1/academics/departments/{id}/
    POST   /api/v1/academics/departments/{id}/archive/
    GET    /api/v1/academics/departments/{id}/courses/
    """
    queryset = Department.objects.select_related('head_of_department', 'created_by').annotate(
        course_count=Count('courses', filter=Q(courses__status='active')),
    ).order_by('name')
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'email']
    ordering_fields = ['code', 'name', 'established_year', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DepartmentWriteSerializer
        if self.action == 'list':
            return DepartmentListSerializer
        return DepartmentDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'archive']:
            return [IsAuthenticated(), IsAdminOrExamStaff()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'status': 'success', 'message': f'Department "{instance.name}" created.', 'data': DepartmentDetailSerializer(instance, context={'request': request}).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_be_deleted():
            return Response(
                {'status': 'error', 'message': 'Cannot delete department. It has associated courses, students, or subjects. Archive it instead.'},
                status=status.HTTP_409_CONFLICT,
            )
        instance.delete()
        return Response({'status': 'success', 'message': f'Department "{instance.name}" deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request, pk=None):
        instance = self.get_object()
        instance.archive(user=request.user)
        return Response({'status': 'success', 'message': f'Department "{instance.name}" archived.'})

    @action(detail=True, methods=['get'], url_path='courses')
    def courses(self, request, pk=None):
        department = self.get_object()
        courses = department.courses.filter(status='active').order_by('code')
        serializer = CourseListSerializer(courses, many=True)
        return Response({'status': 'success', 'data': serializer.data})


class CourseViewSet(viewsets.ModelViewSet):
    """Full CRUD for Course management."""
    queryset = Course.objects.select_related('department', 'created_by').order_by('department__code', 'code')
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'short_name']
    ordering_fields = ['code', 'name', 'duration_years', 'department__code']
    ordering = ['department__code', 'code']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseWriteSerializer
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrExamStaff()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        dept_id = self.request.query_params.get('department')
        status_filter = self.request.query_params.get('status')
        is_pg = self.request.query_params.get('is_postgraduate')
        if dept_id:
            qs = qs.filter(department_id=dept_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if is_pg is not None:
            qs = qs.filter(is_postgraduate=is_pg.lower() in ('true', '1', 'yes'))
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'status': 'success', 'message': f'Course "{instance.name}" created.', 'data': CourseDetailSerializer(instance, context={'request': request}).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_be_deleted():
            return Response(
                {'status': 'error', 'message': 'Cannot delete course with associated branches, semesters, or students.'},
                status=status.HTTP_409_CONFLICT,
            )
        instance.delete()
        return Response({'status': 'success', 'message': f'Course "{instance.name}" deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='branches')
    def branches(self, request, pk=None):
        course = self.get_object()
        branches = course.branches.filter(status='active').order_by('code')
        return Response({'status': 'success', 'data': BranchListSerializer(branches, many=True).data})

    @action(detail=True, methods=['get'], url_path='semesters')
    def semesters(self, request, pk=None):
        course = self.get_object()
        semesters = course.semesters.filter(status='active').order_by('semester_number')
        return Response({'status': 'success', 'data': SemesterListSerializer(semesters, many=True).data})


class BranchViewSet(viewsets.ModelViewSet):
    """Full CRUD for Branch management."""
    queryset = Branch.objects.select_related('course', 'course__department', 'created_by').order_by('course__code', 'code')
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name']
    ordering_fields = ['code', 'name', 'course__code']
    ordering = ['course__code', 'code']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BranchWriteSerializer
        if self.action == 'list':
            return BranchListSerializer
        return BranchDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrExamStaff()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        course_id = self.request.query_params.get('course')
        dept_id = self.request.query_params.get('department')
        status_filter = self.request.query_params.get('status')
        if course_id:
            qs = qs.filter(course_id=course_id)
        if dept_id:
            qs = qs.filter(course__department_id=dept_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'status': 'success', 'message': f'Branch "{instance.name}" created.', 'data': BranchDetailSerializer(instance, context={'request': request}).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_be_deleted():
            return Response(
                {'status': 'error', 'message': 'Cannot delete branch with associated students or semesters.'},
                status=status.HTTP_409_CONFLICT,
            )
        instance.delete()
        return Response({'status': 'success', 'message': f'Branch "{instance.name}" deleted.'}, status=status.HTTP_204_NO_CONTENT)


class SemesterViewSet(viewsets.ModelViewSet):
    """Full CRUD for Semester management."""
    queryset = Semester.objects.select_related(
        'course', 'branch', 'academic_year', 'created_by'
    ).order_by('course__code', 'branch__code', 'semester_number')
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'course__code', 'branch__code']
    ordering_fields = ['semester_number', 'course__code', 'start_date']
    ordering = ['course__code', 'semester_number']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SemesterWriteSerializer
        if self.action == 'list':
            return SemesterListSerializer
        return SemesterDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrExamStaff()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        for param, field in [
            ('course', 'course_id'), ('branch', 'branch_id'),
            ('academic_year', 'academic_year_id'), ('status', 'status'),
            ('semester_number', 'semester_number'),
        ]:
            val = self.request.query_params.get(param)
            if val:
                qs = qs.filter(**{field: val})
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'status': 'success', 'message': f'Semester {instance.semester_number} created.', 'data': SemesterDetailSerializer(instance, context={'request': request}).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_be_deleted():
            return Response(
                {'status': 'error', 'message': 'Cannot delete semester with associated subjects, students, or registrations.'},
                status=status.HTTP_409_CONFLICT,
            )
        instance.delete()
        return Response({'status': 'success', 'message': f'Semester deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='subjects')
    def subjects(self, request, pk=None):
        semester = self.get_object()
        subjects = semester.subjects.filter(status='active').order_by('code')
        return Response({'status': 'success', 'data': SubjectListSerializer(subjects, many=True).data})


class SubjectViewSet(viewsets.ModelViewSet):
    """Full CRUD for Subject management."""
    queryset = Subject.objects.select_related(
        'department', 'course', 'branch', 'semester', 'created_by'
    ).order_by('department__code', 'course__code', 'semester__semester_number', 'code')
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'name', 'short_name']
    ordering_fields = ['code', 'name', 'credits', 'subject_type', 'semester__semester_number']
    ordering = ['code']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SubjectWriteSerializer
        if self.action == 'list':
            return SubjectListSerializer
        return SubjectDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'archive']:
            return [IsAuthenticated(), IsAdminOrExamStaff()]
        return [IsAuthenticated()]

    def get_queryset(self):
        from students.filters import SubjectFilter
        qs = super().get_queryset()
        # Apply dynamic filters
        for param, field in [
            ('department', 'department_id'), ('course', 'course_id'),
            ('branch', 'branch_id'), ('semester', 'semester_id'),
            ('subject_type', 'subject_type'), ('status', 'status'),
            ('semester_number', 'semester__semester_number'),
        ]:
            val = self.request.query_params.get(param)
            if val:
                qs = qs.filter(**{field: val})
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            {'status': 'success', 'message': f'Subject "{instance.name}" created.', 'data': SubjectDetailSerializer(instance, context={'request': request}).data},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.can_be_deleted():
            return Response(
                {'status': 'error', 'message': 'Cannot delete subject with existing registrations.'},
                status=status.HTTP_409_CONFLICT,
            )
        instance.delete()
        return Response({'status': 'success', 'message': f'Subject "{instance.name}" deleted.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], url_path='archive')
    def archive(self, request, pk=None):
        instance = self.get_object()
        instance.archive(user=request.user)
        return Response({'status': 'success', 'message': f'Subject "{instance.name}" archived.'})


class AcademicDashboardView(viewsets.ViewSet):
    """
    GET /api/v1/academics/dashboard/ → Academic management dashboard stats
    GET /api/v1/academics/structure/ → Full academic hierarchy
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        from academics.services import AcademicService
        stats = AcademicService.get_dashboard_stats()
        return Response({'status': 'success', 'data': stats})

    @action(detail=False, methods=['get'], url_path='structure')
    def structure(self, request):
        """Return the full academic hierarchy as a nested structure."""
        from academics.services import AcademicService
        tree = AcademicService.get_academic_tree()
        return Response({'status': 'success', 'data': tree})
