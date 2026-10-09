"""
ExamForge M2 — Registrations ViewSets
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from config.pagination import StandardPagination
from students.permissions import IsAdminOrExamStaff, IsAdminOrExamStaffOrReadOnly

from .models import SubjectRegistration, ExamRegistration, BulkRegistrationJob
from .serializers import (
    SubjectRegistrationSerializer,
    SubjectRegistrationCancelSerializer,
    ExamRegistrationSerializer,
    BulkRegistrationJobSerializer,
    AvailableSubjectSerializer,
)
from .services import RegistrationService, BulkRegistrationService


def success(data, message='', status_code=status.HTTP_200_OK):
    return Response({'success': True, 'message': message, 'data': data}, status=status_code)


# ── Subject Registrations ──────────────────────────────────────
class SubjectRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class   = SubjectRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrExamStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['status', 'academic_year', 'student', 'subject', 'semester']
    search_fields      = [
        'student__full_name', 'student__roll_number',
        'subject__name', 'subject__code',
    ]
    ordering_fields    = ['registration_date', 'created_at', 'status']
    ordering           = ['-registration_date']

    def get_queryset(self):
        user = self.request.user
        qs = SubjectRegistration.objects.select_related(
            'student', 'student__department', 'student__course',
            'subject', 'semester', 'academic_year',
            'registered_by', 'cancelled_by',
        ).all()

        if hasattr(user, 'role') and user.role == 'student':
            qs = qs.filter(student__user=user)

        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(student__full_name__icontains=search) |
                Q(student__roll_number__icontains=search) |
                Q(subject__code__icontains=search) |
                Q(subject__name__icontains=search)
            )
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return success(
            self.get_serializer(instance).data,
            'Subject registration created successfully.',
            status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrExamStaff])
    def cancel(self, request, pk=None):
        instance = self.get_object()
        if instance.status == 'cancelled':
            return Response({'success': False, 'message': 'Registration is already cancelled.'}, status=400)
        ser = SubjectRegistrationCancelSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        instance.cancel(cancelled_by=request.user, reason=ser.validated_data.get('reason', ''))
        return success(self.get_serializer(instance).data, 'Registration cancelled.')

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        return success(RegistrationService.get_dashboard_data())

    @action(detail=False, methods=['get'])
    def available_subjects(self, request):
        student_id = request.query_params.get('student')
        if not student_id:
            return Response({'success': False, 'message': 'student parameter is required.'}, status=400)
        subjects = RegistrationService.get_available_subjects(student_id)
        return success(subjects)


# ── Exam Registrations ────────────────────────────────────────
class ExamRegistrationViewSet(viewsets.ModelViewSet):
    serializer_class   = ExamRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrExamStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['status', 'academic_year', 'student', 'subject', 'exam_session_id']
    search_fields      = [
        'student__full_name', 'student__roll_number',
        'subject__code', 'subject__name',
    ]
    ordering = ['-registration_date']

    def get_queryset(self):
        user = self.request.user
        qs = ExamRegistration.objects.select_related(
            'student', 'subject', 'academic_year',
            'registered_by',
        ).all()
        if hasattr(user, 'role') and user.role == 'student':
            qs = qs.filter(student__user=user)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return success(
            self.get_serializer(instance).data,
            'Exam registration created.',
            status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrExamStaff])
    def cancel(self, request, pk=None):
        instance = self.get_object()
        if instance.status == 'cancelled':
            return Response({'success': False, 'message': 'Already cancelled.'}, status=400)
        reason = request.data.get('reason', 'Cancelled by staff')
        instance.cancel(cancelled_by=request.user, reason=reason)
        return success(self.get_serializer(instance).data, 'Exam registration cancelled.')


# ── Bulk Registration ─────────────────────────────────────────
class BulkRegistrationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = BulkRegistrationJobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrExamStaff]
    pagination_class   = StandardPagination
    filter_backends    = [filters.OrderingFilter]
    ordering           = ['-created_at']

    def get_queryset(self):
        return BulkRegistrationJob.objects.select_related('academic_year', 'created_by').all()

    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'success': False, 'message': 'No file uploaded.'}, status=400)
        reg_type = request.data.get('type', 'subject')
        ac_year  = request.data.get('academic_year_id')
        if not ac_year:
            return Response({'success': False, 'message': 'academic_year_id is required.'}, status=400)
        try:
            job = BulkRegistrationService.process_csv(file, reg_type, ac_year, created_by=request.user)
            ser = BulkRegistrationJobSerializer(job)
            msg = f"Import {job.status}: {job.successful_rows} registered, {job.failed_rows} failed, {job.duplicate_rows} duplicates."
            return success(ser.data, msg, status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({'success': False, 'message': str(exc)}, status=400)


# ── Reports ───────────────────────────────────────────────────
class RegistrationReportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminOrExamStaff]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        ac_year = request.query_params.get('academic_year')
        return success(RegistrationService.get_summary_report(ac_year))

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        ac_year = request.query_params.get('academic_year')
        return success(RegistrationService.get_dept_report(ac_year))
