"""
ExamForge M2 — Student Management API Views
=============================================
ViewSets for all student management endpoints.
All views use M1's authentication system.
All business logic delegated to StudentService.
"""

import logging
import csv
from datetime import datetime

from django.http import HttpResponse, StreamingHttpResponse
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from django.core.exceptions import ValidationError

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from students.models import Student, StudentImportLog, EnrollmentRecord
from students.serializers import (
    StudentListSerializer,
    StudentDetailSerializer,
    StudentWriteSerializer,
    StudentImportLogSerializer,
    EnrollmentRecordSerializer,
    StudentDashboardSerializer,
)
from students.services import StudentService
from students.filters import StudentFilter, EnrollmentRecordFilter
from students.permissions import (
    IsAdminOrExamStaff,
    IsAdminOrExamStaffOrReadOnly,
    CanImportStudents,
    CanViewStudent,
)
from config.pagination import StandardResultsPagination, LargeResultsPagination

logger = logging.getLogger(__name__)


class StudentViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD ViewSet for Student management.

    Endpoints:
      GET    /api/v1/students/           → List all students (paginated, filtered)
      POST   /api/v1/students/           → Create a new student
      GET    /api/v1/students/{id}/      → Retrieve student detail
      PATCH  /api/v1/students/{id}/      → Update student
      DELETE /api/v1/students/{id}/      → Archive student (soft delete)

    Extra actions:
      GET    /api/v1/students/dashboard/         → Dashboard statistics
      POST   /api/v1/students/import/            → CSV bulk import
      GET    /api/v1/students/import/template/   → Download CSV template
      GET    /api/v1/students/import/logs/       → Import history
      GET    /api/v1/students/{id}/summary/      → Individual student summary
      POST   /api/v1/students/{id}/deactivate/   → Deactivate student
      POST   /api/v1/students/{id}/activate/     → Reactivate student
      GET    /api/v1/students/{id}/registrations/ → Student registrations
    """

    queryset = (
        Student.objects
        .select_related(
            'department', 'course', 'branch',
            'current_semester', 'academic_year',
            'created_by', 'updated_by',
        )
        .order_by('roll_number')
    )
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = StudentFilter
    search_fields = [
        'roll_number', 'student_id', 'full_name',
        'first_name', 'last_name', 'institutional_email',
    ]
    ordering_fields = [
        'roll_number', 'full_name', 'admission_year',
        'created_at', 'department__code', 'course__code',
    ]
    ordering = ['roll_number']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StudentWriteSerializer
        if self.action == 'list':
            return StudentListSerializer
        return StudentDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminOrExamStaff]
        elif self.action in ['import_students', 'download_template']:
            permission_classes = [IsAuthenticated, CanImportStudents]
        else:
            permission_classes = [IsAuthenticated, CanViewStudent]
        return [p() for p in permission_classes]

    def get_queryset(self):
        """Apply role-based queryset filtering."""
        qs = super().get_queryset()
        user = self.request.user

        # Students can only see their own record
        if hasattr(user, 'role') and user.role == 'student':
            if hasattr(user, 'student_profile'):
                return qs.filter(pk=user.student_profile.pk)
            return qs.none()

        # Faculty see only their department (or all if admin)
        if hasattr(user, 'role') and user.role == 'faculty':
            dept = getattr(user, 'department_id', None)
            if dept:
                return qs.filter(department_id=dept)

        return qs

    def create(self, request, *args, **kwargs):
        """Create a new student record."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        detail_serializer = StudentDetailSerializer(
            student, context={'request': request}
        )
        logger.info(
            'Student created: %s by %s',
            student.roll_number, request.user.username
        )
        return Response(
            {
                'status': 'success',
                'message': f'Student "{student.full_name}" created successfully.',
                'data': detail_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """Update a student record (full or partial)."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        student = serializer.save()
        detail_serializer = StudentDetailSerializer(
            student, context={'request': request}
        )
        return Response(
            {
                'status': 'success',
                'message': f'Student "{student.full_name}" updated successfully.',
                'data': detail_serializer.data,
            }
        )

    def destroy(self, request, *args, **kwargs):
        """
        Soft-delete (archive) a student record.
        Hard deletion is not permitted if the student has registration records.
        """
        student = self.get_object()
        reason = request.data.get('reason', 'Deleted by administrator.')

        # Check for dependent registrations
        has_registrations = (
            student.subject_registrations.exists()
            or student.exam_registrations.exists()
        )
        if has_registrations:
            # Soft archive instead of delete
            student.deactivate(reason=reason, user=request.user)
            return Response(
                {
                    'status': 'success',
                    'message': (
                        'Student has existing registration records and cannot be permanently '
                        'deleted. The student has been deactivated instead.'
                    ),
                },
                status=status.HTTP_200_OK,
            )

        student_name = student.full_name
        student.delete()
        logger.info(
            'Student %s permanently deleted by %s',
            student_name, request.user.username
        )
        return Response(
            {'status': 'success', 'message': f'Student "{student_name}" deleted permanently.'},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard(self, request):
        """Real-data dashboard statistics for student management."""
        stats = StudentService.get_dashboard_stats(request.user)
        return Response({'status': 'success', 'data': stats})

    @action(
        detail=False,
        methods=['post'],
        url_path='import',
        parser_classes=[MultiPartParser, FormParser],
    )
    def import_students(self, request):
        """
        Import students from a CSV file.

        Expects:
          - file: the CSV file (multipart/form-data)
          - academic_year_id: ID of the target academic year

        Returns a detailed import log with row-level results.
        """
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'status': 'error', 'message': 'No file uploaded. Please provide a CSV file.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        academic_year_id = request.data.get('academic_year_id')
        if not academic_year_id:
            return Response(
                {'status': 'error', 'message': 'academic_year_id is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from academics.models import AcademicYear
        try:
            academic_year = AcademicYear.objects.get(pk=academic_year_id)
        except AcademicYear.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Academic year not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate the file
        is_valid, error_msg, rows = StudentService.validate_csv_file(file)
        if not is_valid:
            return Response(
                {'status': 'error', 'message': error_msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Process the import
        log = StudentService.process_student_import(
            rows=rows,
            academic_year=academic_year,
            imported_by=request.user,
            file_name=file.name,
        )

        serializer = StudentImportLogSerializer(log)
        http_status = (
            status.HTTP_201_CREATED
            if log.failed_rows == 0
            else status.HTTP_207_MULTI_STATUS
        )
        return Response(
            {
                'status': 'success' if log.failed_rows == 0 else 'partial',
                'message': log.summary,
                'data': serializer.data,
            },
            status=http_status,
        )

    @action(detail=False, methods=['get'], url_path='import/template')
    def download_template(self, request):
        """Download the CSV import template."""
        content = StudentService.get_csv_template_content()
        response = HttpResponse(content, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_import_template.csv"'
        return response

    @action(detail=False, methods=['get'], url_path='import/logs')
    def import_logs(self, request):
        """List all import logs for this user (admins see all)."""
        logs = StudentImportLog.objects.all().order_by('-started_at')
        if hasattr(request.user, 'role') and request.user.role != 'admin':
            logs = logs.filter(imported_by=request.user)
        serializer = StudentImportLogSerializer(logs, many=True)
        return Response({'status': 'success', 'data': serializer.data})

    @action(detail=True, methods=['get'], url_path='summary')
    def summary(self, request, pk=None):
        """Comprehensive student summary including registration counts."""
        student = self.get_object()
        summary = StudentService.get_student_summary(str(student.pk))
        detail = StudentDetailSerializer(
            summary['student'], context={'request': request}
        )
        return Response({
            'status': 'success',
            'data': {
                **detail.data,
                'subject_registrations_count': summary['subject_registrations_count'],
                'exam_registrations_count': summary['exam_registrations_count'],
                'enrollment_history': summary['enrollment_history'],
                'can_register_for_exam': summary['can_register_for_exam'],
                'eligibility_reason': summary['eligibility_reason'],
            }
        })

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        """Deactivate a student account."""
        student = self.get_object()
        reason = request.data.get('reason', 'Deactivated by administrator.')
        if not reason.strip():
            return Response(
                {'status': 'error', 'message': 'A reason for deactivation is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        student.deactivate(reason=reason, user=request.user)
        return Response({
            'status': 'success',
            'message': f'Student "{student.full_name}" has been deactivated.',
        })

    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, pk=None):
        """Reactivate a previously deactivated student."""
        student = self.get_object()
        student.status = 'active'
        student.updated_by = request.user
        student.save(update_fields=['status', 'updated_by', 'updated_at'])
        return Response({
            'status': 'success',
            'message': f'Student "{student.full_name}" has been activated.',
        })

    @action(detail=True, methods=['get'], url_path='registrations')
    def registrations(self, request, pk=None):
        """List all subject and exam registrations for a student."""
        student = self.get_object()
        from registrations.serializers import (
            SubjectRegistrationListSerializer,
            ExamRegistrationListSerializer,
        )
        subject_regs = student.subject_registrations.select_related(
            'subject', 'academic_year', 'semester'
        ).order_by('-registration_date')
        exam_regs = student.exam_registrations.select_related(
            'subject', 'academic_year'
        ).order_by('-registration_date')

        return Response({
            'status': 'success',
            'data': {
                'subject_registrations': SubjectRegistrationListSerializer(
                    subject_regs, many=True
                ).data,
                'exam_registrations': ExamRegistrationListSerializer(
                    exam_regs, many=True
                ).data,
            }
        })


class EnrollmentRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for student enrollment history records.

    Endpoints:
      GET    /api/v1/students/enrollments/         → List all enrollment records
      POST   /api/v1/students/enrollments/         → Create enrollment record
      GET    /api/v1/students/enrollments/{id}/    → Detail
      PATCH  /api/v1/students/enrollments/{id}/    → Update
    """

    queryset = EnrollmentRecord.objects.select_related(
        'student', 'semester', 'academic_year', 'created_by'
    ).order_by('-enrolled_date')
    serializer_class = EnrollmentRecordSerializer
    permission_classes = [IsAuthenticated, IsAdminOrExamStaff]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EnrollmentRecordFilter
    search_fields = ['student__roll_number', 'student__full_name']
    ordering_fields = ['enrolled_date', 'student__roll_number']
    ordering = ['-enrolled_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = serializer.save(created_by=request.user)
        return Response(
            {'status': 'success', 'message': 'Enrollment record created.', 'data': serializer.data},
            status=status.HTTP_201_CREATED,
        )
