from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ExamSession, TimeSlot, ExamSubject
from .serializers import ExamSessionSerializer, TimeSlotSerializer, ExamSubjectSerializer
from apps.academics.models import Subject

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.filter(is_active=True)
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamSessionViewSet(viewsets.ModelViewSet):
    queryset = ExamSession.objects.all()
    serializer_class = ExamSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_subjects(self, request, pk=None):
        session = self.get_object()
        subject_ids = request.data.get('subject_ids', [])
        if not subject_ids:
            # If no specific subjects passed, optionally add all subjects matching semester/active
            subject_ids = list(Subject.objects.values_list('id', flat=True))

        added_count = 0
        for sid in subject_ids:
            obj, created = ExamSubject.objects.get_or_create(
                exam_session=session,
                subject_id=sid
            )
            if created:
                added_count += 1

        return Response({
            'message': f'Successfully enrolled {added_count} subjects to {session.name}',
            'total_subjects': session.exam_subjects.count()
        })

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        session = self.get_object()
        session.status = ExamSession.Status.APPROVED
        session.save()
        return Response({'message': f'Session {session.session_code} approved successfully.'})

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        session = self.get_object()
        session.status = ExamSession.Status.PUBLISHED
        session.save()
        return Response({'message': f'Session {session.session_code} is now PUBLISHED and live.'})


class ExamSubjectViewSet(viewsets.ModelViewSet):
    queryset = ExamSubject.objects.select_related('exam_session', 'subject', 'time_slot').all()
    serializer_class = ExamSubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        session_id = self.request.query_params.get('exam_session')
        is_scheduled = self.request.query_params.get('is_scheduled')
        if session_id:
            qs = qs.filter(exam_session_id=session_id)
        if is_scheduled is not None:
            qs = qs.filter(is_scheduled=is_scheduled.lower() == 'true')
        return qs
