from rest_framework import viewsets, filters, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from .models import (
    ExamSession, TimeSlot, ExamSubjectConfig,
    SchedulingConstraintConfig, ExamSessionHistory, SessionStatus
)
from .serializers import (
    ExamSessionSerializer, ExamSessionDetailSerializer,
    TimeSlotSerializer, ExamSubjectConfigSerializer,
    SchedulingConstraintConfigSerializer, ExamSessionHistorySerializer
)
from apps.academics.models import Subject
from apps.accounts.permissions import IsStaffOrAdmin, IsAdminUserRole

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all().order_by('sort_order', 'start_time')
    serializer_class = TimeSlotSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]


class ExamSessionViewSet(viewsets.ModelViewSet):
    queryset = ExamSession.objects.all().order_by('-start_date')
    serializer_class = ExamSessionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'academic_year']
    ordering_fields = ['start_date', 'status', 'name']

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return ExamSessionDetailSerializer
        return ExamSessionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_val = self.request.query_params.get('status')
        academic_year = self.request.query_params.get('academic_year')
        term = self.request.query_params.get('term')
        if status_val:
            qs = qs.filter(status=status_val)
        if academic_year:
            qs = qs.filter(academic_year=academic_year)
        if term:
            qs = qs.filter(term=term)
        return qs

    def perform_create(self, serializer):
        session = serializer.save(created_by=self.request.user)
        # Create default constraint config
        SchedulingConstraintConfig.objects.create(session=session)
        # Record session history
        ExamSessionHistory.objects.create(
            session=session,
            user=self.request.user,
            action='SESSION_CREATED',
            state_from='',
            state_to=SessionStatus.DRAFT,
            details={'message': f"Session {session.name} initialized in Draft mode."}
        )

    @action(detail=True, methods=['post'], url_path='populate-subjects')
    def populate_subjects(self, request, pk=None):
        """
        Auto-populates ExamSubjectConfig records for the session
        based on active subjects in the institution.
        """
        session = self.get_object()
        if session.is_locked:
            return Response({'success': False, 'message': 'Cannot modify subjects in an approved or published session.'}, status=400)

        department_id = request.data.get('department_id')
        semester_number = request.data.get('semester_number')

        subjects_qs = Subject.objects.filter(is_active=True)
        if department_id:
            subjects_qs = subjects_qs.filter(department_id=department_id)
        if semester_number:
            subjects_qs = subjects_qs.filter(semester_number=semester_number)

        added_count = 0
        with transaction.atomic():
            for subj in subjects_qs:
                cfg, created = ExamSubjectConfig.objects.get_or_create(
                    session=session,
                    subject=subj,
                    defaults={
                        'expected_students_count': 60,
                        'max_marks': subj.total_marks,
                        'passing_marks': subj.passing_marks,
                        'question_paper_code': f"QP-{subj.code}-{session.academic_year[:4]}",
                        'difficulty_weight': 4 if subj.difficulty == 'HARD' else 3,
                        'is_practical': subj.subject_type in ['PRACTICAL', 'INTEGRATED']
                    }
                )
                if created:
                    added_count += 1

        ExamSessionHistory.objects.create(
            session=session,
            user=request.user,
            action='SUBJECTS_POPULATED',
            details={'added_subjects': added_count, 'total_now': session.configured_subjects.count()}
        )

        return Response({
            'success': True,
            'message': f"Successfully configured {added_count} subjects for this exam session.",
            'total_configured': session.configured_subjects.count()
        })

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_session(self, request, pk=None):
        """
        Approves an exam session timetable, moving status to APPROVED.
        Controller of Exams or Admin only.
        """
        session = self.get_object()
        if not (request.user.role == 'ADMIN' or request.user.is_superuser):
            return Response({'success': False, 'message': 'Only the Administrator or Exam Controller can approve sessions.'}, status=403)

        if not hasattr(session, 'timetable') or not session.timetable.is_conflict_free:
            return Response({'success': False, 'message': 'Cannot approve a session without a validated, conflict-free timetable.'}, status=400)

        old_status = session.status
        session.status = SessionStatus.APPROVED
        session.approved_by = request.user
        session.save()

        # Also update timetable status
        session.timetable.status = 'APPROVED'
        session.timetable.save()

        ExamSessionHistory.objects.create(
            session=session,
            user=request.user,
            action='SESSION_APPROVED',
            state_from=old_status,
            state_to=SessionStatus.APPROVED,
            details={'approved_by': request.user.get_full_name() or request.user.username}
        )

        return Response({'success': True, 'message': f'Exam session {session.code} approved successfully.', 'status': session.status})

    @action(detail=True, methods=['post'], url_path='publish')
    def publish_session(self, request, pk=None):
        """
        Publishes the timetable to students, faculty, and campus noticeboards.
        """
        session = self.get_object()
        if not (request.user.role == 'ADMIN' or request.user.is_superuser):
            return Response({'success': False, 'message': 'Only the Administrator can publish examination timetables.'}, status=403)

        if session.status != SessionStatus.APPROVED:
            return Response({'success': False, 'message': 'Session must be approved before publishing.'}, status=400)

        old_status = session.status
        session.status = SessionStatus.PUBLISHED
        session.published_at = timezone.now()
        session.save()

        session.timetable.status = 'PUBLISHED'
        session.timetable.published_at = timezone.now()
        session.timetable.save()

        ExamSessionHistory.objects.create(
            session=session,
            user=request.user,
            action='SESSION_PUBLISHED',
            state_from=old_status,
            state_to=SessionStatus.PUBLISHED,
            details={'published_at': str(session.published_at)}
        )

        return Response({'success': True, 'message': f'Exam session {session.code} published to all students and faculty.', 'status': session.status})


class ExamSubjectConfigViewSet(viewsets.ModelViewSet):
    queryset = ExamSubjectConfig.objects.all().order_by('subject__semester_number', 'subject__code')
    serializer_class = ExamSubjectConfigSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        session_id = self.request.query_params.get('session')
        if session_id:
            qs = qs.filter(session_id=session_id)
        return qs

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]


class SchedulingConstraintConfigViewSet(viewsets.ModelViewSet):
    queryset = SchedulingConstraintConfig.objects.all()
    serializer_class = SchedulingConstraintConfigSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsStaffOrAdmin()]
        return [IsAuthenticated()]
